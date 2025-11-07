from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from .models import (
    Category, Product, ProductImage, ProductSpecification, ProductVariant,
    Cart, CartItem, Order, OrderItem, OrderFile
)
class EmailOnlyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Authenticate users strictly with email + password."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Replace the default username field with email to control validation errors
        self.fields['email'] = serializers.EmailField()
        self.fields.pop('username', None)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email:
            raise serializers.ValidationError({'email': 'Email is required.'})

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist as exc:
            raise AuthenticationFailed('No active account found with the provided email.') from exc

        if not user.is_active:
            raise AuthenticationFailed('No active account found with the provided email.')

        credentials = {
            self.username_field: getattr(user, user.USERNAME_FIELD),
            'password': password,
        }

        return super().validate(credentials)


User = get_user_model()


# User Serializers
class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone', 'address', 'city', 
            'state', 'country', 'company_name'
        )
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'address', 'city', 'state', 'country', 'company_name',
            'date_joined', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'username', 'date_joined', 'created_at', 'updated_at')
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile"""
    
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'phone', 'address', 
            'city', 'state', 'country', 'company_name'
        )


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change"""
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs


# Category Serializers
class CategorySerializer(serializers.ModelSerializer):
    """Serializer for categories"""
    products_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = (
            'id', 'name', 'slug', 'description', 'image', 'parent', 
            'is_active', 'order', 'products_count', 'created_at', 'updated_at'
        )
        read_only_fields = ('created_at', 'updated_at')
    
    def get_products_count(self, obj):
        return obj.products.filter(is_active=True).count()


class CategoryListSerializer(serializers.ModelSerializer):
    """Simplified serializer for category lists"""
    
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'image', 'is_active')


# Product Related Serializers
class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for product images"""
    
    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'alt_text', 'order', 'created_at')
        read_only_fields = ('created_at',)


class ProductSpecificationSerializer(serializers.ModelSerializer):
    """Serializer for product specifications"""
    
    class Meta:
        model = ProductSpecification
        fields = ('id', 'key', 'value', 'order')


class ProductVariantSerializer(serializers.ModelSerializer):
    """Serializer for product variants"""
    
    class Meta:
        model = ProductVariant
        fields = (
            'id', 'name', 'sku', 'price_adjustment', 'stock_quantity', 
            'is_active', 'created_at'
        )
        read_only_fields = ('created_at',)


# Product Serializers
class ProductListSerializer(serializers.ModelSerializer):
    """Simplified serializer for product lists"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    current_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Product
        fields = (
            'id', 'name', 'slug', 'category', 'category_name', 'category_slug',
            'short_description', 'price', 'sale_price', 'current_price',
            'main_image', 'in_stock', 'is_featured', 'created_at'
        )


class ProductDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single product"""
    category = CategoryListSerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), 
        source='category', 
        write_only=True
    )
    images = ProductImageSerializer(many=True, read_only=True)
    specifications = ProductSpecificationSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    current_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Product
        fields = (
            'id', 'name', 'slug', 'category', 'category_id', 'description', 
            'short_description', 'price', 'sale_price', 'current_price',
            'stock_quantity', 'track_inventory', 'in_stock', 'sku', 'weight',
            'main_image', 'images', 'specifications', 'variants',
            'is_active', 'is_featured', 'meta_title', 'meta_description',
            'created_at', 'updated_at'
        )
        read_only_fields = ('created_at', 'updated_at')


# Cart Serializers
class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for cart items"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_slug = serializers.CharField(source='product.slug', read_only=True)
    product_image = serializers.ImageField(source='product.main_image', read_only=True)
    variant_name = serializers.CharField(source='variant.name', read_only=True, allow_null=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = CartItem
        fields = (
            'id', 'product', 'product_name', 'product_slug', 'product_image',
            'variant', 'variant_name', 'quantity', 'price', 'total_price',
            'created_at', 'updated_at'
        )
        read_only_fields = ('price', 'created_at', 'updated_at')
    
    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value


class CartSerializer(serializers.ModelSerializer):
    """Serializer for shopping cart"""
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Cart
        fields = (
            'id', 'user', 'items', 'total_items', 'subtotal',
            'created_at', 'updated_at'
        )
        read_only_fields = ('user', 'created_at', 'updated_at')


class AddToCartSerializer(serializers.Serializer):
    """Serializer for adding items to cart"""
    product_id = serializers.IntegerField(required=True)
    variant_id = serializers.IntegerField(required=False, allow_null=True)
    quantity = serializers.IntegerField(default=1, min_value=1)
    
    def validate_product_id(self, value):
        if not Product.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError("Product not found or is inactive.")
        return value
    
    def validate_variant_id(self, value):
        if value and not ProductVariant.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError("Variant not found or is inactive.")
        return value


class UpdateCartItemSerializer(serializers.Serializer):
    """Serializer for updating cart item quantity"""
    quantity = serializers.IntegerField(min_value=1, required=True)


# Order File Serializer
class OrderFileSerializer(serializers.ModelSerializer):
    """Serializer for order file attachments"""
    file_size_mb = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderFile
        fields = (
            'id', 'file', 'file_name', 'file_type', 'file_size', 
            'file_size_mb', 'product_name', 'description', 'uploaded_at'
        )
        read_only_fields = ('uploaded_at',)
    
    def get_file_size_mb(self, obj):
        return round(obj.file_size / (1024 * 1024), 2)


# Order Item Serializers
class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for order items"""
    
    class Meta:
        model = OrderItem
        fields = (
            'id', 'product', 'product_name', 'variant', 'variant_name',
            'quantity', 'price', 'total'
        )
        read_only_fields = ('total',)


class OrderItemDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for order items"""
    product_slug = serializers.CharField(source='product.slug', read_only=True, allow_null=True)
    product_image = serializers.ImageField(source='product.main_image', read_only=True, allow_null=True)
    
    class Meta:
        model = OrderItem
        fields = (
            'id', 'product', 'product_name', 'product_slug', 'product_image',
            'variant', 'variant_name', 'quantity', 'price', 'total'
        )


# Order Serializers
class OrderListSerializer(serializers.ModelSerializer):
    """Simplified serializer for order lists"""
    full_name = serializers.CharField(read_only=True)
    items_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = (
            'id', 'order_number', 'full_name', 'email', 'phone',
            'status', 'payment_status', 'total', 'items_count',
            'created_at', 'updated_at'
        )
        read_only_fields = ('order_number', 'created_at', 'updated_at')
    
    def get_items_count(self, obj):
        return obj.items.count()


class OrderDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single order"""
    items = OrderItemDetailSerializer(many=True, read_only=True)
    files = OrderFileSerializer(many=True, read_only=True)
    full_name = serializers.CharField(read_only=True)
    full_address = serializers.CharField(read_only=True)
    
    class Meta:
        model = Order
        fields = (
            'id', 'order_number', 'user', 'first_name', 'last_name', 'full_name',
            'email', 'phone', 'company_name', 'address_line_1', 'address_line_2',
            'city', 'state', 'country', 'postal_code', 'full_address',
            'order_notes', 'subtotal', 'shipping_cost', 'tax', 'total',
            'status', 'payment_status', 'items', 'files',
            'created_at', 'updated_at', 'confirmed_at', 'shipped_at', 'delivered_at'
        )
        read_only_fields = (
            'order_number', 'user', 'created_at', 'updated_at',
            'confirmed_at', 'shipped_at', 'delivered_at'
        )


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating orders"""
    items = OrderItemSerializer(many=True, required=True)
    
    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'email', 'phone', 'company_name',
            'address_line_1', 'address_line_2', 'city', 'state', 
            'country', 'postal_code', 'order_notes', 'items'
        )
    
    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Order must contain at least one item.")
        return value
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        # Calculate totals
        subtotal = sum(item['price'] * item['quantity'] for item in items_data)
        
        # Create order
        order = Order.objects.create(
            user=self.context['request'].user if self.context['request'].user.is_authenticated else None,
            subtotal=subtotal,
            total=subtotal,  # Add shipping and tax calculation here if needed
            **validated_data
        )
        
        # Create order items
        for item_data in items_data:
            # Get product name if not provided
            if 'product_name' not in item_data and 'product' in item_data:
                item_data['product_name'] = item_data['product'].name
            
            # Get variant name if variant provided
            if 'variant' in item_data and item_data['variant'] and 'variant_name' not in item_data:
                item_data['variant_name'] = item_data['variant'].name
            
            OrderItem.objects.create(order=order, **item_data)
        
        return order


class CheckoutSerializer(serializers.Serializer):
    """Serializer for checkout process"""
    # Billing information
    first_name = serializers.CharField(max_length=100, required=True)
    last_name = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(max_length=20, required=True)
    company_name = serializers.CharField(max_length=200, required=False, allow_blank=True)
    
    # Shipping address
    address_line_1 = serializers.CharField(max_length=300, required=True)
    address_line_2 = serializers.CharField(max_length=300, required=False, allow_blank=True)
    city = serializers.CharField(max_length=100, required=True)
    state = serializers.CharField(max_length=100, required=False, allow_blank=True)
    country = serializers.CharField(max_length=100, required=True)
    postal_code = serializers.CharField(max_length=20, required=False, allow_blank=True)
    
    # Order notes
    order_notes = serializers.CharField(required=False, allow_blank=True)


class OrderStatusUpdateSerializer(serializers.Serializer):
    """Serializer for updating order status"""
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES, required=True)


class PaymentStatusUpdateSerializer(serializers.Serializer):
    """Serializer for updating payment status"""
    payment_status = serializers.ChoiceField(choices=Order.PAYMENT_STATUS_CHOICES, required=True)

