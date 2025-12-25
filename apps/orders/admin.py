"""
Admin configuration for orders app
"""
from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Order, OrderItem, OrderDocument, OrderStatusHistory


class OrderItemInline(admin.TabularInline):
    """Inline for order items"""
    model = OrderItem
    extra = 0
    readonly_fields = ('total',)
    fields = ('product_name', 'variant_name', 'quantity', 'price', 'total')


class OrderDocumentInline(admin.TabularInline):
    """Inline for order documents"""
    model = OrderDocument
    extra = 0
    readonly_fields = ('file', 'file_name', 'doc_type', 'file_size', 'uploaded_at')
    fields = ('file', 'file_name', 'doc_type', 'product_name', 'uploaded_at')
    can_delete = False


class OrderStatusHistoryInline(admin.TabularInline):
    """Inline for order status history"""
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('status', 'notes', 'changed_by', 'created_at')
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
    
    inlines = [OrderItemInline, OrderDocumentInline, OrderStatusHistoryInline]
    
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
        count = 0
        products_to_update = set()
        
        for order in queryset.filter(status='shipped'):
            old_status = order.status
            order.status = 'delivered'
            if not order.delivered_at:
                order.delivered_at = timezone.now()
            order.save()  # This will trigger product sold count updates via save() method
            count += 1
        
        self.message_user(request, f'{count} order(s) marked as delivered.')
    mark_as_delivered.short_description = 'Mark selected as Delivered'
    
    def mark_as_paid(self, request, queryset):
        """Bulk action to mark orders as paid"""
        count = queryset.update(payment_status='paid')
        self.message_user(request, f'{count} order(s) marked as paid.')
    mark_as_paid.short_description = 'Mark selected as Paid'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Order item administration"""
    list_display = ('id', 'order', 'product_name', 'quantity', 'price', 'total')
    list_filter = ('order__created_at',)
    search_fields = ('product_name', 'order__order_number')
    readonly_fields = ('total',)


@admin.register(OrderDocument)
class OrderDocumentAdmin(admin.ModelAdmin):
    """Order document administration"""
    list_display = ('id', 'order', 'doc_type', 'file_name', 'file_size', 'uploaded_at')
    list_filter = ('doc_type', 'uploaded_at')
    search_fields = ('file_name', 'order__order_number', 'product_name')
    readonly_fields = ('file_size', 'uploaded_at')


@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    """Order status history administration"""
    list_display = ('order', 'status', 'changed_by', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order__order_number', 'notes')
    readonly_fields = ('created_at',)

