"""
Authentication endpoints
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from apps.accounts import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.EmailTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('profile/', views.get_user_profile, name='profile'),
    path('profile/update/', views.update_user_profile, name='profile-update'),
    path('change-password/', views.change_password, name='change-password'),
]

