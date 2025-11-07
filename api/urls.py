from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    # Authentication
    register_user, get_user_profile, update_user_profile, change_password,
    EmailTokenObtainPairView,
    # ViewSets
    CategoryViewSet, ProductViewSet,
    ProductImageViewSet, ProductSpecificationViewSet, ProductVariantViewSet,
    CartViewSet, OrderViewSet,
    # Admin
    admin_statistics,
)

# Create router for ViewSets
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'product-images', ProductImageViewSet, basename='product-image')
router.register(r'product-specifications', ProductSpecificationViewSet, basename='product-specification')
router.register(r'product-variants', ProductVariantViewSet, basename='product-variant')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', register_user, name='register'),
    path('auth/login/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User profile endpoints
    path('auth/profile/', get_user_profile, name='user-profile'),
    path('auth/profile/update/', update_user_profile, name='user-profile-update'),
    path('auth/change-password/', change_password, name='change-password'),
    
    # Admin endpoints
    path('admin/statistics/', admin_statistics, name='admin-statistics'),
    
    # Include router URLs (this creates all REST endpoints)
    path('', include(router.urls)),
]

# Available endpoints from router:
# - /categories/ and /categories/{slug}/
# - /products/ and /products/{slug}/
# - /cart/ and /cart/{id}/
# - /orders/ and /orders/{id}/
# - /product-images/, /product-specifications/, /product-variants/ (admin)

