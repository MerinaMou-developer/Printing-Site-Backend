"""
Cart endpoints
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.cart import views

router = DefaultRouter()
router.register(r'cart', views.CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
]

