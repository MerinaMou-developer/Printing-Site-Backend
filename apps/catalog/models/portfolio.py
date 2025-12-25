"""
Portfolio Model
"""
from django.db import models
from .service import Service


class Portfolio(models.Model):
    """Portfolio/Gallery items"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='portfolio_items'
    )
    image = models.ImageField(upload_to='portfolio/')
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_featured', '-created_at']
        verbose_name = 'Portfolio Item'
        verbose_name_plural = 'Portfolio Items'
    
    def __str__(self):
        return self.title

