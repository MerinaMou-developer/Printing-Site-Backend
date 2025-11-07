from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, FileExtensionValidator
import uuid


# Custom User Model with extended fields
class User(AbstractUser):
    """Extended user model with additional fields for customer information"""
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.username


# Category Model
class Category(models.Model):
    """Product categories for organizing stamps, printing services, etc."""
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        related_name='children'
    )
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Display order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


# Product Model
class Product(models.Model):
    """Products including stamps, banners, printing services, etc."""
    name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True)
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products'
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
        ]
    
    def __str__(self):
        return self.name
    
    @property
    def current_price(self):
        """Return sale price if available, otherwise regular price"""
        if self.sale_price and self.sale_price < self.price:
            return self.sale_price
        return self.price


# Additional Product Images
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


# Product Specifications
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


# Product Variants (e.g., colors, sizes)
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


# Cart Model
class Cart(models.Model):
    """Shopping cart for authenticated and guest users"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=200, blank=True, null=True)  # For guest users
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        if self.user:
            return f"Cart - {self.user.username}"
        return f"Guest Cart - {self.session_id}"
    
    @property
    def total_items(self):
        """Total number of items in cart"""
        return sum(item.quantity for item in self.items.all())
    
    @property
    def subtotal(self):
        """Cart subtotal"""
        return sum(item.total_price for item in self.items.all())


# Cart Item Model
class CartItem(models.Model):
    """Individual items in the shopping cart"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(
        ProductVariant, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Price at the time of adding to cart"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    @property
    def total_price(self):
        """Total price for this cart item"""
        return self.price * self.quantity
    
    def save(self, *args, **kwargs):
        """Set price from product if not provided"""
        if not self.price:
            base_price = self.product.current_price
            if self.variant:
                base_price += self.variant.price_adjustment
            self.price = base_price
        super().save(*args, **kwargs)


# Order Model
class Order(models.Model):
    """Customer orders"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('ready', 'Ready'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    # Order identification
    order_number = models.CharField(max_length=50, unique=True, editable=False)
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='orders'
    )
    
    # Customer information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    
    # Shipping address
    address_line_1 = models.CharField(max_length=300)
    address_line_2 = models.CharField(max_length=300, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    
    # Order details
    order_notes = models.TextField(blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(
        max_length=20, 
        choices=PAYMENT_STATUS_CHOICES, 
        default='pending'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['user', 'status']),
        ]
    
    def __str__(self):
        return f"Order {self.order_number}"
    
    def save(self, *args, **kwargs):
        """Generate order number if not exists"""
        if not self.order_number:
            # Generate unique order number: ORD-YYYYMMDD-UUID
            from datetime import datetime
            date_str = datetime.now().strftime('%Y%m%d')
            unique_id = str(uuid.uuid4())[:8].upper()
            self.order_number = f"ORD-{date_str}-{unique_id}"
        super().save(*args, **kwargs)
    
    @property
    def full_name(self):
        """Customer full name"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_address(self):
        """Complete formatted address"""
        parts = [
            self.address_line_1,
            self.address_line_2,
            self.city,
            self.state,
            self.country,
            self.postal_code
        ]
        return ", ".join(filter(None, parts))


# Order Item Model
class OrderItem(models.Model):
    """Individual items in an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=300)  # Store name in case product is deleted
    variant = models.ForeignKey(
        ProductVariant, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    variant_name = models.CharField(max_length=200, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
    
    def save(self, *args, **kwargs):
        """Calculate total"""
        self.total = self.price * self.quantity
        super().save(*args, **kwargs)


# Order File Attachments
class OrderFile(models.Model):
    """File attachments for orders (design files, etc.)"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(
        upload_to='orders/%Y/%m/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'jpg', 'jpeg', 'png', 'ai', 'eps', 'psd', 'cdr', 'svg']
            )
        ]
    )
    file_name = models.CharField(max_length=300)
    file_type = models.CharField(max_length=50)  # emiratesId, tradeLicense, specificDesign, etc.
    file_size = models.PositiveBigIntegerField()  # Size in bytes
    product_name = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.order.order_number} - {self.file_name}"
