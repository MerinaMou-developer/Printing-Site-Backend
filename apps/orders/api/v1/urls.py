"""
Order endpoints
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.orders import views

router = DefaultRouter()
router.register(r'orders', views.OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]

