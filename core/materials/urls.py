from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MaterialViewSet

router = DefaultRouter()
router.register(r'materials', MaterialViewSet, basename='materials')
urlpatterns = [path("", include(router.urls))]
