from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TeacherMaterialViewSet, StudentMaterialViewSet

router = DefaultRouter()
router.register(r'teacher/materials', TeacherMaterialViewSet, basename='materials')
router.register(r'student/materials', StudentMaterialViewSet, basename='materials')
urlpatterns = [
    path("", include(router.urls))
]
