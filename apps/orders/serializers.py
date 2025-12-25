"""
Order Serializers
"""
from rest_framework import serializers
from apps.orders.models import (
    Order, OrderItem, OrderDocument,
    STATUS_CHOICES, PAYMENT_STATUS_CHOICES
)


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


class OrderDocumentSerializer(serializers.ModelSerializer):
    """Serializer for order documents"""
    file_size_mb = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderDocument
        fields = (
            'id', 'file', 'file_name', 'doc_type', 'file_size', 
            'file_size_mb', 'product_name', 'description', 'uploaded_at'
        )
        read_only_fields = ('uploaded_at',)
    
    def get_file_size_mb(self, obj):
        return round(obj.file_size / (1024 * 1024), 2)


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
    documents = OrderDocumentSerializer(many=True, read_only=True)
    full_name = serializers.CharField(read_only=True)
    full_address = serializers.CharField(read_only=True)
    
    class Meta:
        model = Order
        fields = (
            'id', 'order_number', 'user', 'first_name', 'last_name', 'full_name',
            'email', 'phone', 'company_name', 'address_line_1', 'address_line_2',
            'city', 'state', 'country', 'postal_code', 'full_address',
            'order_notes', 'subtotal', 'shipping_cost', 'tax', 'total',
            'status', 'payment_status', 'items', 'documents',
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
    status = serializers.ChoiceField(choices=STATUS_CHOICES, required=True)


class PaymentStatusUpdateSerializer(serializers.Serializer):
    """Serializer for updating payment status"""
    payment_status = serializers.ChoiceField(choices=PAYMENT_STATUS_CHOICES, required=True)

