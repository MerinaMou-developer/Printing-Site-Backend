"""
Product Requirement Model (kept separate for clarity)
"""
from django.db import models
from .product import Product

DOCUMENT_TYPE_CHOICES = [
    ('EMIRATES_ID', 'Emirates ID'),
    ('TRADE_LICENSE', 'Trade License'),
    ('DESIGN', 'Design File'),
    ('OTHER', 'Other'),
]


class ProductRequirement(models.Model):
    """Document requirements for products"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='requirements'
    )
    doc_type = models.CharField(
        max_length=50,
        choices=DOCUMENT_TYPE_CHOICES
    )
    is_required = models.BooleanField(default=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'doc_type']
        unique_together = ['product', 'doc_type']
    
    def __str__(self):
        return f"{self.product.name} - {self.get_doc_type_display()}"

