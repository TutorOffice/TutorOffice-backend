from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HomeworkViewSet, LessonTeacherViewSet, LessonStudentViewSet

router = DefaultRouter()

router.register(r'homeworks', HomeworkViewSet, basename='homeworks')
router.register(r'lessons_teachers', LessonTeacherViewSet, basename='lessons_teachers')
router.register(r'lessons_students', LessonStudentViewSet, basename='lessons_students')
urlpatterns = [path("", include(router.urls))]
