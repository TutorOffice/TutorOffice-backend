from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HomeworkViewSet, LessonViewSet

router = DefaultRouter()

router.register(r"homeworks", HomeworkViewSet, basename="homeworks")
router.register(r"lessons", LessonViewSet, basename="lessons")
urlpatterns = [path("", include(router.urls)),]