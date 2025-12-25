"""
Catalog API v1 endpoints
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.catalog.views import (
    ProductViewSet,
    CategoryViewSet,
    CompanyView,
    ServiceViewSet,
    PortfolioViewSet,
    ClientViewSet
)

# Public endpoints router (no auth required)
public_router = DefaultRouter()
public_router.register(r'categories', CategoryViewSet, basename='category')
public_router.register(r'services', ServiceViewSet, basename='service')
public_router.register(r'products', ProductViewSet, basename='product')  # Products are now public for read
public_router.register(r'portfolio', PortfolioViewSet, basename='portfolio')
public_router.register(r'clients', ClientViewSet, basename='client')

urlpatterns = [
    # Public endpoints
    path('company/', CompanyView.as_view(), name='company'),
    path('', include(public_router.urls)),
]

