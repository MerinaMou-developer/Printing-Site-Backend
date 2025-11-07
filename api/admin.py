from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import (
    User, Category, Product, ProductImage, ProductSpecification, ProductVariant,
    Cart, CartItem, Order, OrderItem, OrderFile
)


# ============ User Admin ============

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Enhanced user admin with additional fields"""
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone', 'is_staff', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'company_name')
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('phone', 'address', 'city', 'state', 'country', 'company_name')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('email', 'phone', 'first_name', 'last_name')
        }),
    )


# ============ Category Admin ============

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category administration"""
    list_display = ('name', 'slug', 'parent', 'is_active', 'order', 'products_count', 'created_at')
    list_filter = ('is_active', 'parent', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')
    list_editable = ('is_active', 'order')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'image')
        }),
        ('Hierarchy', {
            'fields': ('parent',)
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
    )
    
    def products_count(self, obj):
        """Display number of products in category"""
        return obj.products.filter(is_active=True).count()
    products_count.short_description = 'Products'


# ============ Product Related Inlines ============

class ProductImageInline(admin.TabularInline):
    """Inline for additional product images"""
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'order')


class ProductSpecificationInline(admin.TabularInline):
    """Inline for product specifications"""
    model = ProductSpecification
    extra = 1
    fields = ('key', 'value', 'order')


class ProductVariantInline(admin.TabularInline):
    """Inline for product variants"""
    model = ProductVariant
    extra = 1
    fields = ('name', 'sku', 'price_adjustment', 'stock_quantity', 'is_active')


# ============ Product Admin ============

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Product administration with enhanced features"""
    list_display = (
        'name', 'category', 'price_display', 'stock_display', 
        'in_stock', 'is_featured', 'is_active', 'created_at'
    )
    list_filter = (
        'category', 'is_active', 'is_featured', 'in_stock', 
        'track_inventory', 'created_at'
    )
    search_fields = ('name', 'description', 'sku')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('-created_at',)
    list_editable = ('is_active', 'is_featured', 'in_stock')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'description', 'short_description')
        }),
        ('Pricing', {
            'fields': ('price', 'sale_price')
        }),
        ('Inventory', {
            'fields': ('stock_quantity', 'track_inventory', 'in_stock', 'sku', 'weight')
        }),
        ('Media', {
            'fields': ('main_image',)
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [ProductImageInline, ProductSpecificationInline, ProductVariantInline]
    
    def price_display(self, obj):
        """Display price with sale price if available"""
        if obj.sale_price and obj.sale_price < obj.price:
            return format_html(
                '<span style="text-decoration: line-through; color: #999;">{}</span> '
                '<span style="color: #28a745; font-weight: bold;">{}</span>',
                f'AED {obj.price}',
                f'AED {obj.sale_price}'
            )
        return f'AED {obj.price}'
    price_display.short_description = 'Price'
    
    def stock_display(self, obj):
        """Display stock with color coding"""
        if obj.track_inventory:
            if obj.stock_quantity <= 0:
                color = 'red'
            elif obj.stock_quantity < 10:
                color = 'orange'
            else:
                color = 'green'
            return format_html(
                '<span style="color: {}; font-weight: bold;">{}</span>',
                color,
                obj.stock_quantity
            )
        return 'N/A'
    stock_display.short_description = 'Stock'


# ============ Cart Admin ============

class CartItemInline(admin.TabularInline):
    """Inline for cart items"""
    model = CartItem
    extra = 0
    readonly_fields = ('total_price',)
    fields = ('product', 'variant', 'quantity', 'price', 'total_price')


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


# ============ Order Admin ============

class OrderItemInline(admin.TabularInline):
    """Inline for order items"""
    model = OrderItem
    extra = 0
    readonly_fields = ('total',)
    fields = ('product_name', 'variant_name', 'quantity', 'price', 'total')


class OrderFileInline(admin.TabularInline):
    """Inline for order files"""
    model = OrderFile
    extra = 0
    readonly_fields = ('file', 'file_name', 'file_type', 'file_size', 'uploaded_at')
    fields = ('file', 'file_name', 'file_type', 'product_name', 'uploaded_at')
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Order administration with enhanced features"""
    list_display = (
        'order_number', 'full_name', 'email', 'phone', 
        'status_display', 'payment_status_display', 'total_display', 'created_at'
    )
    list_filter = (
        'status', 'payment_status', 'created_at', 
        'confirmed_at', 'shipped_at', 'delivered_at'
    )
    search_fields = (
        'order_number', 'first_name', 'last_name', 
        'email', 'phone', 'company_name'
    )
    readonly_fields = (
        'order_number', 'created_at', 'updated_at', 
        'confirmed_at', 'shipped_at', 'delivered_at'
    )
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'payment_status')
        }),
        ('Customer Information', {
            'fields': (
                'first_name', 'last_name', 'email', 'phone', 'company_name'
            )
        }),
        ('Shipping Address', {
            'fields': (
                'address_line_1', 'address_line_2', 'city', 
                'state', 'country', 'postal_code'
            )
        }),
        ('Order Details', {
            'fields': ('order_notes', 'subtotal', 'shipping_cost', 'tax', 'total')
        }),
        ('Timestamps', {
            'fields': (
                'created_at', 'updated_at', 'confirmed_at', 
                'shipped_at', 'delivered_at'
            ),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [OrderItemInline, OrderFileInline]
    
    def status_display(self, obj):
        """Display status with color coding"""
        colors = {
            'pending': '#ffc107',
            'confirmed': '#17a2b8',
            'processing': '#007bff',
            'ready': '#28a745',
            'shipped': '#6610f2',
            'delivered': '#28a745',
            'cancelled': '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_display.short_description = 'Status'
    
    def payment_status_display(self, obj):
        """Display payment status with color coding"""
        colors = {
            'pending': '#ffc107',
            'paid': '#28a745',
            'failed': '#dc3545',
            'refunded': '#6c757d',
        }
        color = colors.get(obj.payment_status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-weight: bold;">{}</span>',
            color,
            obj.get_payment_status_display()
        )
    payment_status_display.short_description = 'Payment'
    
    def total_display(self, obj):
        """Display order total"""
        return format_html(
            '<span style="font-weight: bold; color: #28a745;">AED {}</span>',
            f'{obj.total:.2f}'
        )
    total_display.short_description = 'Total'
    
    actions = ['mark_as_confirmed', 'mark_as_shipped', 'mark_as_delivered', 'mark_as_paid']
    
    def mark_as_confirmed(self, request, queryset):
        """Bulk action to confirm orders"""
        from django.utils import timezone
        count = 0
        for order in queryset:
            if order.status == 'pending':
                order.status = 'confirmed'
                order.confirmed_at = timezone.now()
                order.save()
                count += 1
        self.message_user(request, f'{count} order(s) marked as confirmed.')
    mark_as_confirmed.short_description = 'Mark selected as Confirmed'
    
    def mark_as_shipped(self, request, queryset):
        """Bulk action to mark orders as shipped"""
        from django.utils import timezone
        count = 0
        for order in queryset.filter(status__in=['confirmed', 'processing', 'ready']):
            order.status = 'shipped'
            order.shipped_at = timezone.now()
            order.save()
            count += 1
        self.message_user(request, f'{count} order(s) marked as shipped.')
    mark_as_shipped.short_description = 'Mark selected as Shipped'
    
    def mark_as_delivered(self, request, queryset):
        """Bulk action to mark orders as delivered"""
        from django.utils import timezone
        count = 0
        for order in queryset.filter(status='shipped'):
            order.status = 'delivered'
            order.delivered_at = timezone.now()
            order.save()
            count += 1
        self.message_user(request, f'{count} order(s) marked as delivered.')
    mark_as_delivered.short_description = 'Mark selected as Delivered'
    
    def mark_as_paid(self, request, queryset):
        """Bulk action to mark orders as paid"""
        count = queryset.update(payment_status='paid')
        self.message_user(request, f'{count} order(s) marked as paid.')
    mark_as_paid.short_description = 'Mark selected as Paid'


# Customize admin site header
admin.site.site_header = "PrintPro Administration"
admin.site.site_title = "PrintPro Admin"
admin.site.index_title = "Welcome to PrintPro Administration"
