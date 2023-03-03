from clients.views import RegisterView
from rest_framework import routers
from django.urls import path, include


router = routers.DefaultRouter()
router.register('register', RegisterView)

urlpatterns = [
    path('', include(router.urls))
]
