"""
Order Models
"""
from django.db import models
from django.core.validators import MinValueValidator, FileExtensionValidator
import uuid
from common.utils import generate_order_number
from apps.accounts.models import User
from apps.catalog.models.product import Product, ProductVariant

# Document Type Choices
DOCUMENT_TYPE_CHOICES = [
    ('EMIRATES_ID', 'Emirates ID'),
    ('TRADE_LICENSE', 'Trade License'),
    ('DESIGN', 'Design File'),
    ('OTHER', 'Other'),
]

# Order Status Choices
STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('processing', 'Processing'),
    ('ready', 'Ready'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
]

# Payment Status Choices
PAYMENT_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('paid', 'Paid'),
    ('failed', 'Failed'),
    ('refunded', 'Refunded'),
]


class Order(models.Model):
    """Customer orders"""
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
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
    
    def __str__(self):
        return f"Order {self.order_number}"
    
    def save(self, *args, **kwargs):
        """Generate order number if not exists and track status changes"""
        # Track old status before saving
        old_status = None
        if self.pk:
            try:
                old_order = Order.objects.get(pk=self.pk)
                old_status = old_order.status
            except Order.DoesNotExist:
                pass
        
        # Generate order number if not exists
        if not self.order_number:
            self.order_number = generate_order_number()
        
        super().save(*args, **kwargs)
        
        # Update product sold counts if status changed to/from delivered
        if old_status is not None:
            new_status = self.status
            if (old_status != new_status and 
                (new_status == 'delivered' or old_status == 'delivered')):
                # Update sold counts for all products in this order
                products_to_update = set()
                for item in self.items.all():
                    if item.product:
                        products_to_update.add(item.product)
                
                for product in products_to_update:
                    product.update_sold_count()
    
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


class OrderItem(models.Model):
    """Individual items in an order"""
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='items'
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.SET_NULL, 
        null=True
    )
    product_name = models.CharField(max_length=300)  # Store name in case product is deleted
    variant = models.ForeignKey(
        ProductVariant, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    variant_name = models.CharField(max_length=200, blank=True, null=True)
    quantity = models.PositiveIntegerField(
        default=1, 
        validators=[MinValueValidator(1)]
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
    
    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
    
    def save(self, *args, **kwargs):
        """Calculate total"""
        self.total = self.price * self.quantity
        super().save(*args, **kwargs)


class OrderDocument(models.Model):
    """Documents attached to orders (copied from cart documents)"""
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='documents'
    )
    order_item = models.ForeignKey(
        OrderItem,
        on_delete=models.CASCADE,
        related_name='documents',
        null=True,
        blank=True
    )
    doc_type = models.CharField(
        max_length=50,
        choices=DOCUMENT_TYPE_CHOICES
    )
    file = models.FileField(
        upload_to='orders/%Y/%m/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'jpg', 'jpeg', 'png', 'ai', 'eps', 'psd', 'cdr', 'svg', 'doc', 'docx']
            )
        ]
    )
    file_name = models.CharField(max_length=300)
    file_size = models.PositiveBigIntegerField()  # Size in bytes
    product_name = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Order Document'
        verbose_name_plural = 'Order Documents'
    
    def __str__(self):
        return f"{self.order.order_number} - {self.file_name}"


class OrderStatusHistory(models.Model):
    """Track order status changes"""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='status_history'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    notes = models.TextField(blank=True, null=True)
    changed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order Status History'
        verbose_name_plural = 'Order Status Histories'
    
    def __str__(self):
        return f"{self.order.order_number} - {self.status}"

