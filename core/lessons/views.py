from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter
from .models import Homework, Lesson
from .serializers import HomeworkSerializer,  LessonTeacherSerializer, LessonStudentSerializer
from clients.models import Teacher, Student, TeacherStudent
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .filters import LessonFilter
from clients.permissions import IsTeacherOwnerOrIsStaffPermission


class HomeworkViewSet(ModelViewSet):
    """ViewSet для эндпойнта /homeworks/
    c пагинацией и поиском по полю title"""

    serializer_class = HomeworkSerializer
    queryset = Homework.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ('title',)
#   pagination_class = LimitOffsetPagination
    permission_classes = [IsTeacherOwnerOrIsStaffPermission]


class LessonTeacherViewSet(ModelViewSet):
    """ViewSet для эндпойнта /lessons_teachers/
    c пагинацией и кастомной фильтрацией"""

    serializer_class = LessonTeacherSerializer
    http_method_names = ['get', 'patch', 'post', 'delete']
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_class = LessonFilter
    search_fields = ('data',)
    #   pagination_class = LimitOffsetPagination
    permission_classes = [IsTeacherOwnerOrIsStaffPermission]

    def get_queryset(self):
        """Получения queryset уроков  учителя"""
        teacher = get_object_or_404(Teacher,
                                    user=self.request.user)
        return teacher.lessons.all()

    def perform_create(self, serializer):
        """Метод предопределения автора."""
        teacher = get_object_or_404(Teacher,
                                    user=self.request.user)
        serializer.save(teacher=teacher)


class LessonStudentViewSet(ReadOnlyModelViewSet):
    """ViewSet для эндпойнта /lessons_students/
    c пагинацией и фильтрации по дате и теме урока"""

    serializer_class = LessonStudentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Метод обработки запроса."""
        #student = get_object_or_404(Student, user=self.request.user)
        return Lesson.objects.filter(teacher_student__email=self.request.user.email)
