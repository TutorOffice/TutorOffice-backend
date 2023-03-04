from django.urls import path, include
from rest_framework import routers
from clients.views import RegisterView
from .views import SendEmailView, ActivateUserView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

router = routers.DefaultRouter()
router.register('register', RegisterView)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/email-verify/<str:uid>/', SendEmailView.as_view(), name='verify'),
    path('auth/user-activate/<str:token>/', ActivateUserView.as_view(), name='activate'),
    path('', include(router.urls))
]
