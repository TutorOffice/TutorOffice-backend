from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (DetailTeacherLessonViewSet, DetailStudentLessonViewSet,
                    ListLessonViewSet, AggregateLessonsViewSet)
# HomeworkStudentViewSet, HomeworkTeacherViewSet,

router = DefaultRouter()
# router.register(r'homeworks_students',
#                 HomeworkStudentViewSet,
#                 basename='homeworks_students')
# router.register(r'homeworks_teachers',
#                 HomeworkTeacherViewSet,
#                 basename='homeworks_teachers')
router.register(r'user/lessons/number',
                AggregateLessonsViewSet,
                basename='lessons_number')
router.register(r'user/lessons/list',
                ListLessonViewSet,
                basename='lessons')
router.register(r'teacher/lesson',
                DetailTeacherLessonViewSet,
                basename='teacher_lesson')
router.register(r'student/lesson',
                DetailStudentLessonViewSet,
                basename='student_lesson')

urlpatterns = [path("", include(router.urls))]
