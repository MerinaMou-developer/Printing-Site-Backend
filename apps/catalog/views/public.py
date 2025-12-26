"""
Public Website Views - No Authentication Required
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from apps.catalog.models import Company, Service, ServiceItem, Portfolio, Client
from apps.catalog.serializers import (
    CompanySerializer, ServiceSerializer, ServiceDetailSerializer,
    PortfolioSerializer, ClientSerializer
)


class CompanyView(APIView):
    """Company profile endpoint"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Get company profile"""
        company = Company.objects.first()
        if not company:
            return Response(
                {'error': 'Company profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = CompanySerializer(company)
        return Response(serializer.data)


class ServiceViewSet(viewsets.ModelViewSet):
    """
    Service endpoints
    
    GET /api/v1/services/ - List all services (public)
    GET /api/v1/services/{id}/ - Get service details with items (public)
    GET /api/v1/services/{id}/products/ - Get products for this service (Public - No Auth)
    POST /api/v1/services/ - Create service (admin only)
    PUT /api/v1/services/{id}/ - Update service (admin only)
    PATCH /api/v1/services/{id}/ - Partial update service (admin only)
    DELETE /api/v1/services/{id}/ - Delete service (admin only)
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    lookup_field = 'id'
    
    def get_permissions(self):
        """Allow read access to everyone, write access to admins only"""
        if self.action in ['list', 'retrieve', 'products']:
            permission_classes = [AllowAny]  # Public access
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """Filter active services for list, show all for admin"""
        if self.action == 'list' and not self.request.user.is_staff:
            return Service.objects.filter(is_active=True)
        return Service.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ServiceDetailSerializer
        return ServiceSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """Get service with items"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def products(self, request, id=None):
        """Get all products for this service (Public - No Auth)"""
        from apps.catalog.models import Product
        from apps.catalog.serializers.product import ProductListSerializer
        from django.db.models import Q
        
        service = self.get_object()
        products = Product.objects.filter(
            service=service,
            is_active=True
        ).select_related('category', 'service').prefetch_related('images', 'requirements')
        
        # Apply search filter
        search = request.query_params.get('search', None)
        if search:
            products = products.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )
        
        # Apply category filter
        category_id = request.query_params.get('category', None)
        if category_id:
            try:
                products = products.filter(category_id=int(category_id))
            except (ValueError, TypeError):
                pass  # Invalid category ID, ignore it
        
        # Pagination
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductListSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)


class PortfolioViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Portfolio/Gallery endpoints
    
    GET /api/v1/portfolio/ - List portfolio items
    GET /api/v1/portfolio/?service_id={id} - Filter by service
    GET /api/v1/portfolio/{id}/ - Get portfolio item details
    """
    queryset = Portfolio.objects.filter(is_active=True)
    serializer_class = PortfolioSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        service_id = self.request.query_params.get('service_id', None)
        if service_id:
            queryset = queryset.filter(service_id=service_id)
        return queryset


class ClientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Client logos endpoints
    
    GET /api/v1/clients/ - List all client logos
    """
    queryset = Client.objects.filter(is_active=True)
    serializer_class = ClientSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

