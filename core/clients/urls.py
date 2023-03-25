from django.urls import path, include
from rest_framework import routers
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
from django.contrib.auth.views import (
    PasswordResetDoneView, PasswordResetCompleteView
)

register_router = routers.DefaultRouter()
register_router.register('register', RegisterView, basename='register')


urlpatterns = [
    path('', include(register_router.urls)),
    path('login/',
         TokenObtainPairView.as_view(),
         name='login'),
    path('refresh/',
         TokenRefreshView.as_view(),
         name='refresh'),
    path('auth/user-activate/<str:token>/',
         ActivateUserView.as_view(),
         name='activate'),
    path('profile/',
         ProfileViewSet.as_view({'get': 'retrieve',
                                 'patch': 'update'}),
         name='profile',),
    path('password-reset/', CustomPasswordResetView.as_view(),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/',
         CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('subjects/',
         SubjectsView.as_view(),
         name='subjects'),
    path('user-subjects/',
         UserSubjectViewSet.as_view({'get': 'list', 'put': 'update',
                                     'post': 'create'}),
         name='user_subjects'),
]
