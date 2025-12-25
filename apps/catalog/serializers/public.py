"""
Public API Serializers
"""
from rest_framework import serializers
from django.utils.text import slugify
from apps.catalog.models import Company, Service, ServiceItem, Portfolio, Client


class CompanySerializer(serializers.ModelSerializer):
    """Company profile serializer"""
    socials = serializers.SerializerMethodField()
    
    class Meta:
        model = Company
        fields = (
            'name', 'phone', 'whatsapp', 'email', 'address',
            'about_text', 'logo', 'socials'
        )
    
    def get_socials(self, obj):
        """Return social media links"""
        socials = {}
        if obj.facebook:
            socials['facebook'] = obj.facebook
        if obj.instagram:
            socials['instagram'] = obj.instagram
        if obj.twitter:
            socials['twitter'] = obj.twitter
        if obj.linkedin:
            socials['linkedin'] = obj.linkedin
        return socials if socials else None


class ServiceItemSerializer(serializers.ModelSerializer):
    """Service item serializer"""
    
    class Meta:
        model = ServiceItem
        fields = (
            'id', 'name', 'slug', 'description', 'image',
            'is_active', 'order'
        )


class ServiceSerializer(serializers.ModelSerializer):
    """Service list serializer with auto-generated slug"""
    slug = serializers.SlugField(required=False, allow_blank=True)
    
    class Meta:
        model = Service
        fields = (
            'id', 'name', 'slug', 'description', 'image',
            'is_active', 'order'
        )
        extra_kwargs = {
            'slug': {'required': False},  # Slug can be auto-generated
        }
    
    def create(self, validated_data):
        """Auto-generate slug from name if not provided"""
        if not validated_data.get('slug'):
            validated_data['slug'] = self._generate_unique_slug(validated_data['name'])
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """Auto-generate slug from name if name changed and slug not provided"""
        if 'name' in validated_data and not validated_data.get('slug'):
            validated_data['slug'] = self._generate_unique_slug(
                validated_data['name'], 
                instance.pk
            )
        return super().update(instance, validated_data)
    
    def _generate_unique_slug(self, name, instance_pk=None):
        """Generate a unique slug from the service name"""
        base_slug = slugify(name)
        unique_slug = base_slug
        num = 1
        
        # Check if slug already exists (excluding current instance if updating)
        queryset = Service.objects.filter(slug=unique_slug)
        if instance_pk:
            queryset = queryset.exclude(pk=instance_pk)
        
        while queryset.exists():
            unique_slug = f"{base_slug}-{num}"
            queryset = Service.objects.filter(slug=unique_slug)
            if instance_pk:
                queryset = queryset.exclude(pk=instance_pk)
            num += 1
        
        return unique_slug


class ServiceDetailSerializer(serializers.ModelSerializer):
    """Service detail serializer with items and auto-generated slug"""
    items = ServiceItemSerializer(many=True, read_only=True)
    slug = serializers.SlugField(required=False, allow_blank=True)
    
    class Meta:
        model = Service
        fields = (
            'id', 'name', 'slug', 'description', 'image',
            'is_active', 'order', 'items', 'created_at', 'updated_at'
        )
        extra_kwargs = {
            'slug': {'required': False},  # Slug can be auto-generated
        }
    
    def create(self, validated_data):
        """Auto-generate slug from name if not provided"""
        if not validated_data.get('slug'):
            validated_data['slug'] = self._generate_unique_slug(validated_data['name'])
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """Auto-generate slug from name if name changed and slug not provided"""
        if 'name' in validated_data and not validated_data.get('slug'):
            validated_data['slug'] = self._generate_unique_slug(
                validated_data['name'], 
                instance.pk
            )
        return super().update(instance, validated_data)
    
    def _generate_unique_slug(self, name, instance_pk=None):
        """Generate a unique slug from the service name"""
        base_slug = slugify(name)
        unique_slug = base_slug
        num = 1
        
        # Check if slug already exists (excluding current instance if updating)
        queryset = Service.objects.filter(slug=unique_slug)
        if instance_pk:
            queryset = queryset.exclude(pk=instance_pk)
        
        while queryset.exists():
            unique_slug = f"{base_slug}-{num}"
            queryset = Service.objects.filter(slug=unique_slug)
            if instance_pk:
                queryset = queryset.exclude(pk=instance_pk)
            num += 1
        
        return unique_slug


class PortfolioSerializer(serializers.ModelSerializer):
    """Portfolio serializer"""
    service_name = serializers.CharField(source='service.name', read_only=True)
    
    class Meta:
        model = Portfolio
        fields = (
            'id', 'title', 'slug', 'description', 'service',
            'service_name', 'image', 'is_featured', 'is_active',
            'created_at', 'updated_at'
        )


class ClientSerializer(serializers.ModelSerializer):
    """Client serializer"""
    
    class Meta:
        model = Client
        fields = (
            'id', 'name', 'logo', 'website', 'is_active', 'order'
        )

