"""
Company Profile Model
"""
from django.db import models


class Company(models.Model):
    """Company profile information"""
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField()
    address = models.TextField()
    about_text = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='company/', blank=True, null=True)
    
    # Social media
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Company'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """Ensure only one company profile exists"""
        if not self.pk and Company.objects.exists():
            existing = Company.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)

