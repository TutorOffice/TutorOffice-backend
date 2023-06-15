from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    StudentHomeworkViewSet,
    StudentMessageViewSet,
    TeacherHomeworkViewSet,
    TeacherMessageViewSet,
                    )
app_name = "chats"

router = DefaultRouter()
router.register(
    r"teacher/homeworks", TeacherHomeworkViewSet, basename="teacher_homeworks"
)
router.register(
    r"student/homeworks", StudentHomeworkViewSet, basename="student_homeworks"
)
router.register(
    r"teacher/messages", TeacherMessageViewSet, basename="teacher_messages"
)
router.register(
    r"student/messages", StudentMessageViewSet, basename="student_messages"
)
urlpatterns = [path("", include(router.urls))]
