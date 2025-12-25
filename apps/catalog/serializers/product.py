"""
Product Serializers
"""
from rest_framework import serializers
from apps.catalog.models import Product, ProductRequirement, Category, Service


class ProductRequirementSerializer(serializers.ModelSerializer):
    """Product requirement serializer"""
    
    class Meta:
        model = ProductRequirement
        fields = ('doc_type', 'is_required', 'description', 'order')


class ProductListSerializer(serializers.ModelSerializer):
    """Product list serializer"""
    category_name = serializers.CharField(source='category.name', read_only=True, allow_null=True)
    service_name = serializers.CharField(source='service.name', read_only=True, allow_null=True)
    current_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Product
        fields = (
            'id', 'name', 'slug', 'category', 'category_name',
            'service', 'service_name',
            'short_description', 'price', 'sale_price', 'current_price',
            'main_image', 'in_stock', 'is_featured', 'total_sold'
        )


class ProductCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating products
    
    Validation:
    - Category is optional if service is provided
    - Service is optional if category is provided
    - At least one of category or service must be provided
    - No automatic category assignment
    """
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=False,
        allow_null=True
    )
    service = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = Product
        fields = (
            'name', 'slug', 'category', 'service',
            'description', 'short_description',
            'price', 'sale_price',
            'stock_quantity', 'track_inventory', 'in_stock',
            'sku', 'weight',
            'main_image',
            'is_active', 'is_featured',
            'meta_title', 'meta_description'
        )
        extra_kwargs = {
            'category': {'required': False, 'allow_null': True},
            'service': {'required': False, 'allow_null': True},
            'sku': {'required': False, 'allow_null': True, 'allow_blank': True},
        }
    
    def validate_slug(self, value):
        """Validate slug uniqueness"""
        if value:
            # Check if slug already exists (excluding current instance if updating)
            queryset = Product.objects.filter(slug=value)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.exists():
                raise serializers.ValidationError(
                    "A product with this slug already exists. Please use a different slug."
                )
        return value
    
    def validate(self, attrs):
        """Validate that at least one of category or service is provided"""
        category = attrs.get('category')
        service = attrs.get('service')
        
        # For update, check existing instance values if not in attrs
        if self.instance:
            if category is None and 'category' not in self.initial_data:
                category = self.instance.category
            if service is None and 'service' not in self.initial_data:
                service = self.instance.service
        
        if not category and not service:
            raise serializers.ValidationError({
                'non_field_errors': ['Either category or service must be provided.']
            })
        
        return attrs
    
    def create(self, validated_data):
        """Create product - no automatic category assignment"""
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """Update product - no automatic category assignment"""
        return super().update(instance, validated_data)


class ProductDetailSerializer(serializers.ModelSerializer):
    """Product detail serializer with requirements"""
    requirements = ProductRequirementSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True, allow_null=True)
    service_name = serializers.CharField(source='service.name', read_only=True, allow_null=True)
    current_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Product
        fields = (
            'id', 'name', 'slug', 'category', 'category_name',
            'service', 'service_name',
            'description', 'short_description', 'price', 'sale_price', 'current_price',
            'stock_quantity', 'in_stock', 'main_image', 'images',
            'requirements', 'is_featured', 'total_sold', 'created_at', 'updated_at'
        )

