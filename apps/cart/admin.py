"""
Admin configuration for cart app
"""
from django.contrib import admin
from .models import Cart, CartItem, CartItemDocument


class CartItemInline(admin.TabularInline):
    """Inline for cart items"""
    model = CartItem
    extra = 0
    readonly_fields = ('total_price',)
    fields = ('product', 'variant', 'quantity', 'price', 'total_price')


class CartItemDocumentInline(admin.TabularInline):
    """Inline for cart item documents"""
    model = CartItemDocument
    extra = 0
    readonly_fields = ('file', 'file_name', 'doc_type', 'file_size', 'uploaded_at')
    fields = ('doc_type', 'file', 'file_name', 'file_size', 'uploaded_at')
    can_delete = True


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Cart administration"""
    list_display = ('id', 'user', 'session_id', 'items_count', 'total_display', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'session_id')
    readonly_fields = ('created_at', 'updated_at', 'total_items', 'subtotal')
    ordering = ('-updated_at',)
    
    inlines = [CartItemInline]
    
    fieldsets = (
        ('Cart Information', {
            'fields': ('user', 'session_id')
        }),
        ('Summary', {
            'fields': ('total_items', 'subtotal', 'created_at', 'updated_at')
        }),
    )
    
    def items_count(self, obj):
        """Display number of items"""
        return obj.items.count()
    items_count.short_description = 'Items'
    
    def total_display(self, obj):
        """Display cart total"""
        return f'AED {obj.subtotal:.2f}'
    total_display.short_description = 'Total'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Cart item administration"""
    list_display = ('id', 'cart', 'product', 'quantity', 'price', 'total_price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('product__name', 'cart__user__username')
    readonly_fields = ('total_price', 'created_at', 'updated_at')
    
    inlines = [CartItemDocumentInline]


@admin.register(CartItemDocument)
class CartItemDocumentAdmin(admin.ModelAdmin):
    """Cart item document administration"""
    list_display = ('id', 'cart_item', 'doc_type', 'file_name', 'file_size', 'uploaded_at')
    list_filter = ('doc_type', 'uploaded_at')
    search_fields = ('file_name', 'cart_item__product__name')
    readonly_fields = ('file_size', 'uploaded_at')

