"""
Cart Serializers
"""
from rest_framework import serializers
from apps.cart.models import Cart, CartItem, CartItemDocument
from apps.catalog.models import Product


class CartItemDocumentSerializer(serializers.ModelSerializer):
    """Cart item document serializer"""
    doc_type_display = serializers.CharField(source='get_doc_type_display', read_only=True)
    
    class Meta:
        model = CartItemDocument
        fields = (
            'id', 'doc_type', 'doc_type_display', 'file', 'file_name',
            'file_size', 'uploaded_at'
        )
        read_only_fields = ('file_name', 'file_size', 'uploaded_at')


class CartItemSerializer(serializers.ModelSerializer):
    """Cart item serializer"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_slug = serializers.CharField(source='product.slug', read_only=True)
    product_image = serializers.ImageField(source='product.main_image', read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    documents = CartItemDocumentSerializer(many=True, read_only=True)
    
    class Meta:
        model = CartItem
        fields = (
            'id', 'product', 'product_name', 'product_slug', 'product_image',
            'quantity', 'price', 'total_price', 'documents', 'created_at', 'updated_at'
        )
        read_only_fields = ('price', 'created_at', 'updated_at')


class CartSerializer(serializers.ModelSerializer):
    """Cart serializer"""
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Cart
        fields = (
            'id', 'items', 'total_items', 'subtotal',
            'created_at', 'updated_at'
        )
        read_only_fields = ('created_at', 'updated_at')


class AddCartItemSerializer(serializers.Serializer):
    """Add item to cart serializer with optional document uploads"""
    product_id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(default=1, min_value=1)
    # Optional document uploads
    emirates_id = serializers.FileField(required=False, allow_null=True)
    trade_license = serializers.FileField(required=False, allow_null=True)
    design = serializers.FileField(required=False, allow_null=True)
    
    def validate_product_id(self, value):
        if not Product.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError("Product not found or is inactive.")
        return value
    
    def validate_emirates_id(self, value):
        """Validate Emirates ID file"""
        if value:
            return self._validate_file(value)
        return value
    
    def validate_trade_license(self, value):
        """Validate Trade License file"""
        if value:
            return self._validate_file(value)
        return value
    
    def validate_design(self, value):
        """Validate Design file"""
        if value:
            return self._validate_file(value)
        return value
    
    def _validate_file(self, value):
        """Common file validation"""
        # Check file size (max 10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("File size cannot exceed 10MB.")
        
        # Check file type
        valid_extensions = ['pdf', 'jpg', 'jpeg', 'png', 'ai', 'eps', 'psd', 'cdr', 'svg', 'doc', 'docx']
        file_extension = value.name.split('.')[-1].lower()
        if file_extension not in valid_extensions:
            raise serializers.ValidationError(
                f"Invalid file format. Allowed: {', '.join(valid_extensions)}"
            )
        
        return value


class UpdateCartItemSerializer(serializers.Serializer):
    """Update cart item quantity serializer"""
    quantity = serializers.IntegerField(min_value=1, required=True)


class UploadDocumentSerializer(serializers.Serializer):
    """Upload document serializer"""
    doc_type = serializers.ChoiceField(
        choices=['EMIRATES_ID', 'TRADE_LICENSE', 'DESIGN', 'OTHER'],
        required=True
    )
    file = serializers.FileField(required=True)
    
    def validate_file(self, value):
        """Validate file"""
        # Check file size (max 10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("File size cannot exceed 10MB.")
        
        # Check file type
        valid_extensions = ['pdf', 'jpg', 'jpeg', 'png', 'ai', 'eps', 'psd', 'cdr', 'svg', 'doc', 'docx']
        file_extension = value.name.split('.')[-1].lower()
        if file_extension not in valid_extensions:
            raise serializers.ValidationError(
                f"Invalid file format. Allowed: {', '.join(valid_extensions)}"
            )
        
        return value


class BulkUploadDocumentsSerializer(serializers.Serializer):
    """Bulk upload documents serializer - upload all documents at once"""
    emirates_id = serializers.FileField(required=False, allow_null=True)
    trade_license = serializers.FileField(required=False, allow_null=True)
    design = serializers.FileField(required=False, allow_null=True)
    
    def validate_emirates_id(self, value):
        """Validate Emirates ID file"""
        if value:
            return self._validate_file(value)
        return value
    
    def validate_trade_license(self, value):
        """Validate Trade License file"""
        if value:
            return self._validate_file(value)
        return value
    
    def validate_design(self, value):
        """Validate Design file"""
        if value:
            return self._validate_file(value)
        return value
    
    def _validate_file(self, value):
        """Common file validation"""
        # Check file size (max 10MB)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("File size cannot exceed 10MB.")
        
        # Check file type
        valid_extensions = ['pdf', 'jpg', 'jpeg', 'png', 'ai', 'eps', 'psd', 'cdr', 'svg', 'doc', 'docx']
        file_extension = value.name.split('.')[-1].lower()
        if file_extension not in valid_extensions:
            raise serializers.ValidationError(
                f"Invalid file format. Allowed: {', '.join(valid_extensions)}"
            )
        
        return value
