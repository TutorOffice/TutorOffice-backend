from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (HomeworkStudentViewSet, HomeworkTeacherViewSet,
                    LessonStudentViewSet, LessonTeacherViewSet)

router = DefaultRouter()
router.register(r'homeworks_students',
                HomeworkStudentViewSet,
                basename='homeworks_students')
router.register(r'homeworks_teachers',
                HomeworkTeacherViewSet,
                basename='homeworks_teachers')
router.register(r'lessons_teachers',
                LessonTeacherViewSet,
                basename='lessons_teachers')
router.register(r'lessons_students',
                LessonStudentViewSet,
                basename='lessons_students')
urlpatterns = [path("", include(router.urls))]
