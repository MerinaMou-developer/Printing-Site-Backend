"""
Category Serializers
"""
from rest_framework import serializers
from django.utils.text import slugify
from apps.catalog.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for categories with auto-generated slug"""
    products_count = serializers.SerializerMethodField()
    slug = serializers.SlugField(required=False, allow_blank=True)
    
    class Meta:
        model = Category
        fields = (
            'id', 'name', 'slug', 'description', 'image', 
            'is_active', 'order', 'products_count', 'created_at', 'updated_at'
        )
        read_only_fields = ('created_at', 'updated_at')
        extra_kwargs = {
            'slug': {'required': False},  # Slug can be auto-generated
        }
    
    def get_products_count(self, obj):
        return obj.products.filter(is_active=True).count()
    
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
        """Generate a unique slug from the category name"""
        base_slug = slugify(name)
        unique_slug = base_slug
        num = 1
        
        # Check if slug already exists (excluding current instance if updating)
        queryset = Category.objects.filter(slug=unique_slug)
        if instance_pk:
            queryset = queryset.exclude(pk=instance_pk)
        
        while queryset.exists():
            unique_slug = f"{base_slug}-{num}"
            queryset = Category.objects.filter(slug=unique_slug)
            if instance_pk:
                queryset = queryset.exclude(pk=instance_pk)
            num += 1
        
        return unique_slug


class CategoryListSerializer(serializers.ModelSerializer):
    """Simplified serializer for category lists"""
    
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'image', 'is_active')

