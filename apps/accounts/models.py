"""
User model - extends Django's AbstractUser
"""
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    """Custom user manager where email is the unique identifier"""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user with email and password"""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser with email and password"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


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
    
    # Use custom manager
    objects = UserManager()
    
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

