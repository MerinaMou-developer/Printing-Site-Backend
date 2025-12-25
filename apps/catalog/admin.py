"""
Admin configuration for catalog app
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, Product, ProductImage, ProductSpecification, ProductVariant,
    ProductRequirement, Company, Service, ServiceItem, Portfolio, Client
)


# ============ Category Admin ============

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category administration"""
    list_display = ('name', 'slug', 'is_active', 'order', 'products_count', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')
    list_editable = ('is_active', 'order')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'image')
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


class ProductRequirementInline(admin.TabularInline):
    """Inline for product document requirements"""
    model = ProductRequirement
    extra = 1
    fields = ('doc_type', 'is_required', 'description', 'order')
    verbose_name = 'Document Requirement'
    verbose_name_plural = 'Document Requirements'


# ============ Product Admin ============

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Product administration with service linking"""
    list_display = (
        'name', 'category', 'service', 'price_display', 'stock_display', 
        'total_sold', 'in_stock', 'is_featured', 'is_active', 'created_at'
    )
    list_filter = (
        'category', 'service', 'is_active', 'is_featured', 'in_stock', 
        'track_inventory', 'created_at'
    )
    search_fields = ('name', 'description', 'sku')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('-created_at',)
    list_editable = ('is_active', 'is_featured', 'in_stock')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'service', 'description', 'short_description')
        }),
        ('Pricing', {
            'fields': ('price', 'sale_price')
        }),
        ('Inventory', {
            'fields': ('stock_quantity', 'track_inventory', 'in_stock', 'total_sold', 'sku', 'weight')
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
    
    inlines = [ProductImageInline, ProductSpecificationInline, ProductVariantInline, ProductRequirementInline]
    
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


# ============ Company Admin ============

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Company administration"""
    list_display = ('name', 'email', 'phone', 'whatsapp', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'phone', 'whatsapp')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'logo', 'about_text')
        }),
        ('Contact Information', {
            'fields': ('phone', 'whatsapp', 'email', 'address')
        }),
        ('Social Media', {
            'fields': ('facebook', 'instagram', 'twitter', 'linkedin'),
            'classes': ('collapse',)
        }),
    )


# ============ Service Admin ============

class ServiceItemInline(admin.TabularInline):
    """Inline for service items"""
    model = ServiceItem
    extra = 1
    fields = ('name', 'slug', 'description', 'image', 'is_active', 'order')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Service administration"""
    list_display = ('name', 'slug', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')
    list_editable = ('is_active', 'order')
    
    inlines = [ServiceItemInline]


# ============ Portfolio Admin ============

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    """Portfolio administration"""
    list_display = ('title', 'slug', 'service', 'is_featured', 'is_active', 'created_at')
    list_filter = ('is_featured', 'is_active', 'service', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)
    list_editable = ('is_featured', 'is_active')


# ============ Client Admin ============

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Client administration"""
    list_display = ('name', 'website', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'website')
    ordering = ('order', 'name')
    list_editable = ('is_active', 'order')

