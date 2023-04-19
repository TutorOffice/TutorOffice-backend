from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TeacherLessonViewSet, StudentLessonViewSet, AggregateLessonsViewSet
# HomeworkStudentViewSet, HomeworkTeacherViewSet,

router = DefaultRouter()
# router.register(r'homeworks_students',
#                 HomeworkStudentViewSet,
#                 basename='homeworks_students')
# router.register(r'homeworks_teachers',
#                 HomeworkTeacherViewSet,
#                 basename='homeworks_teachers')
router.register(r'lessons/number',
                AggregateLessonsViewSet,
                basename='lessons_number')
router.register(r'teacher/lessons',
                TeacherLessonViewSet,
                basename='teacher_lessons')
router.register(r'student/lessons',
                StudentLessonViewSet,
                basename='student_lessons')

urlpatterns = [path("", include(router.urls))]
