from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TeacherMaterialViewSet

router = DefaultRouter()
router.register(r'teacher/materials', TeacherMaterialViewSet, basename='materials')

urlpatterns = [
    path("", include(router.urls))
]
