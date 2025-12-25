"""
Product Views (Public Read, Admin Write)
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from django.db.models import Q

from apps.catalog.models import Product, ProductRequirement
from apps.catalog.serializers import (
    ProductListSerializer, ProductDetailSerializer, ProductCreateSerializer
)


class ProductViewSet(viewsets.ModelViewSet):
    """
    Product endpoints
    
    GET /api/v1/products/ - List all active products (Public - No Auth)
    GET /api/v1/products/{id}/ - Get product by ID (Public - No Auth)
    GET /api/v1/products/{slug}/ - Get product by slug (Public - No Auth)
    POST /api/v1/products/ - Create product (admin only)
    PUT /api/v1/products/{id}/ - Update product by ID (admin only)
    PATCH /api/v1/products/{id}/ - Partial update product by ID (admin only)
    DELETE /api/v1/products/{id}/ - Delete product by ID (admin only)
    
    Note: Slug must be unique when creating products.
    """
    queryset = Product.objects.all().select_related('category', 'service').prefetch_related(
        'images', 'requirements'
    )
    serializer_class = ProductListSerializer
    lookup_field = 'id'  # Default lookup, but get_object() supports both ID and slug
    
    def get_permissions(self):
        """Public access for read, admin required for write"""
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]  # Public access
        else:
            permission_classes = [IsAdminUser]  # Admin only for write
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Filter active products for public, show all for admin"""
        if self.action == 'list':
            # For public users, show only active products
            if not self.request.user.is_staff:
                return Product.objects.filter(is_active=True).select_related('category', 'service').prefetch_related(
                    'images', 'requirements'
                )
        # For admins, show all products (including inactive)
        return Product.objects.all().select_related('category', 'service').prefetch_related(
            'images', 'requirements'
        )
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ProductCreateSerializer
        elif self.action == 'retrieve':
            return ProductDetailSerializer
        elif self.action in ['update', 'partial_update']:
            return ProductCreateSerializer
        return ProductListSerializer
    
    def get_object(self):
        """
        Override to support both ID and slug lookup
        - /api/v1/products/3/ - Uses ID
        - /api/v1/products/my-product-slug/ - Uses slug
        """
        lookup_value = self.kwargs.get(self.lookup_field)
        
        # Try to get by ID first (if it's numeric)
        if lookup_value and str(lookup_value).isdigit():
            try:
                return self.get_queryset().get(id=int(lookup_value))
            except Product.DoesNotExist:
                pass
        
        # If not found by ID or not numeric, try slug
        try:
            return self.get_queryset().get(slug=lookup_value)
        except Product.DoesNotExist:
            # If still not found, raise 404
            from rest_framework.exceptions import NotFound
            raise NotFound('Product not found.')
    
    def retrieve(self, request, *args, **kwargs):
        """Get product with requirements"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

