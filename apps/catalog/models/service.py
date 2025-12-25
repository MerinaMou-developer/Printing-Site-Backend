"""
Service Models
"""
from django.db import models


class Service(models.Model):
    """Main services (Screen Print, DTF, UV, Offset, Signboard, etc.)"""
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
    
    def __str__(self):
        return self.name


class ServiceItem(models.Model):
    """Items under a service (T-shirt print, Mug print, Brochure, etc.)"""
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='items'
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='service-items/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
        unique_together = ['service', 'slug']
        verbose_name = 'Service Item'
        verbose_name_plural = 'Service Items'
    
    def __str__(self):
        return f"{self.service.name} - {self.name}"

