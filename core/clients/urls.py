from django.urls import path, include
from .views import SendEmailView, ActivateUserView

urlpatterns = [
    path('auth/email-verify/<str:uid>/', SendEmailView.as_view(), name='verify'),
    path('auth/user-activate/<str:token>/', ActivateUserView.as_view(), name='activate'),
]