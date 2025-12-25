"""
User model - extends Django's AbstractUser
"""
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Extended user model with additional fields for customer information"""
    # Override username to allow duplicates (email is the unique identifier)
    username = models.CharField(
        max_length=150,
        unique=False,  # Allow duplicate usernames
        blank=True,
        null=False,
        default='',
        help_text="Optional. Can be duplicate. Users login with email."
    )
    # Email is the unique identifier and used for authentication
    email = models.EmailField(unique=True, blank=False, null=False)
    
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Use email as USERNAME_FIELD (allows username to be non-unique)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email is the only required field for createsuperuser
    
    class Meta:
        ordering = ['-date_joined']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        # Ensure email is unique
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_email')
        ]
    
    def __str__(self):
        return self.email or self.username or f"User {self.id}"

