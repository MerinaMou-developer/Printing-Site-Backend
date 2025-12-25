"""
Product Models
"""
from django.db import models
from django.db.models import Sum
from django.core.validators import MinValueValidator
from .category import Category
from .service import Service

# Document Type Choices (moved to common/constants but kept here for model)
DOCUMENT_TYPE_CHOICES = [
    ('EMIRATES_ID', 'Emirates ID'),
    ('TRADE_LICENSE', 'Trade License'),
    ('DESIGN', 'Design File'),
    ('OTHER', 'Other'),
]


class Product(models.Model):
    """Products including stamps, banners, printing services, etc."""
    name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True)
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products',
        blank=True,
        null=True,
        help_text="Optional: Category for stamp products. Required if service is not provided."
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        related_name='products',
        blank=True,
        null=True,
        help_text="Optional: Link product to a service (e.g., Screen Print, DTF)"
    )
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True, null=True)
    
    # Pricing
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)],
        help_text="Base price in AED"
    )
    sale_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True,
        validators=[MinValueValidator(0)],
        help_text="Sale price (optional)"
    )
    
    # Inventory
    stock_quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    track_inventory = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    total_sold = models.IntegerField(
        default=0, 
        validators=[MinValueValidator(0)],
        help_text="Total quantity sold from completed orders"
    )
    
    # Product details
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True)
    weight = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        blank=True, 
        null=True,
        help_text="Weight in kg"
    )
    
    # Images
    main_image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['service', 'is_active']),
        ]
    
    def __str__(self):
        return self.name
    
    @property
    def current_price(self):
        """Return sale price if available, otherwise regular price"""
        if self.sale_price and self.sale_price < self.price:
            return self.sale_price
        return self.price
    
    def save(self, *args, **kwargs):
        """Save product"""
        super().save(*args, **kwargs)
    
    def update_sold_count(self):
        """Update total_sold from completed orders"""
        from apps.orders.models import OrderItem
        # Count quantity from delivered orders only
        total = OrderItem.objects.filter(
            product=self,
            order__status='delivered'
        ).aggregate(
            total=Sum('quantity')
        )['total'] or 0
        self.total_sold = total
        self.save(update_fields=['total_sold'])


class ProductImage(models.Model):
    """Additional images for products"""
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True, null=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.product.name} - Image {self.order}"


class ProductSpecification(models.Model):
    """Specifications for products (e.g., size, material, color options)"""
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='specifications'
    )
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=500)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'key']
    
    def __str__(self):
        return f"{self.product.name} - {self.key}: {self.value}"


class ProductVariant(models.Model):
    """Variants for products like different colors or sizes"""
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='variants'
    )
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True)
    price_adjustment = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        help_text="Additional cost for this variant"
    )
    stock_quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.product.name} - {self.name}"



