"""
Cart Models
"""
from django.db import models
from django.core.validators import MinValueValidator, FileExtensionValidator
from apps.accounts.models import User
from apps.catalog.models.product import Product, ProductVariant

# Document Type Choices
DOCUMENT_TYPE_CHOICES = [
    ('EMIRATES_ID', 'Emirates ID'),
    ('TRADE_LICENSE', 'Trade License'),
    ('DESIGN', 'Design File'),
    ('OTHER', 'Other'),
]


class Cart(models.Model):
    """Shopping cart for authenticated users"""
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='cart'
    )
    session_id = models.CharField(max_length=200, blank=True, null=True)  # For guest users
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
    
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


class CartItem(models.Model):
    """Individual items in the shopping cart"""
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE, 
        related_name='items'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(
        ProductVariant, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    quantity = models.PositiveIntegerField(
        default=1, 
        validators=[MinValueValidator(1)]
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Price at the time of adding to cart"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
    
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


class CartItemDocument(models.Model):
    """Documents uploaded for cart items"""
    cart_item = models.ForeignKey(
        CartItem,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    doc_type = models.CharField(
        max_length=50,
        choices=DOCUMENT_TYPE_CHOICES
    )
    file = models.FileField(
        upload_to='cart-documents/%Y/%m/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'jpg', 'jpeg', 'png', 'ai', 'eps', 'psd', 'cdr', 'svg', 'doc', 'docx']
            )
        ]
    )
    file_name = models.CharField(max_length=300)
    file_size = models.PositiveBigIntegerField()  # Size in bytes
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        unique_together = ['cart_item', 'doc_type']
        verbose_name = 'Cart Item Document'
        verbose_name_plural = 'Cart Item Documents'
    
    def __str__(self):
        return f"{self.cart_item.product.name} - {self.get_doc_type_display()}"

