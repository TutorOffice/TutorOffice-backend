from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AggregateLessonsViewSet,
    DetailStudentLessonViewSet,
    DetailTeacherLessonViewSet,
    ListLessonViewSet,
)

# HomeworkStudentViewSet, HomeworkTeacherViewSet,

app_name = "lessons"

router = DefaultRouter()
router.register(
    r"user/lessons/number", AggregateLessonsViewSet, basename="lesson_number"
)
router.register(r"user/lesson/list", ListLessonViewSet, basename="lesson")
router.register(
    r"teacher/lessons", DetailTeacherLessonViewSet, basename="teacher_lesson"
)
router.register(
    r"student/lessons", DetailStudentLessonViewSet, basename="student_lesson"
)

urlpatterns = [path("", include(router.urls))]
