from django.urls import path, include
from rest_framework import routers
from .views import ActivateUserView, RegisterView, ProfileViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

register_router = routers.DefaultRouter()
register_router.register('register', RegisterView, basename='register')


urlpatterns = [
    path('', include(register_router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('auth/user-activate/<str:token>/', ActivateUserView.as_view(), name='activate'),
    path(
        'profile/',
        ProfileViewSet.as_view({'patch': 'update'}),
        name='update-profile',
    ),
    path(
        'profile/',
        ProfileViewSet.as_view({'get': 'retrieve'}),
        name='profile',
    ),
]
