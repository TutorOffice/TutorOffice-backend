from clients.models import Teacher
from clients.permissions import IsTeacherOwner, IsTeacher
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import LessonFilter # HomeworkFilter,
from .models import Homework, Lesson
from .serializers import (HomeworkStudentSerializer, HomeworkTeacherSerializer,
                          LessonSerializer)


# class HomeworkTeacherViewSet(ModelViewSet):
#     """ViewSet для эндпойнта /homeworks_teachers/
#     c пагинацией и поиском по полю title"""
#
#     serializer_class = HomeworkTeacherSerializer
#     http_method_names = ['get', 'patch', 'post', 'delete']
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = HomeworkFilter
#     permission_classes = [IsAuthenticated,
#                           IsTeacherOwner]
#
#     def get_queryset(self):
#         """Получения queryset домашних заданий  учителя"""
#         teacher = get_object_or_404(Teacher,
#                                     user=self.request.user)
#         return teacher.homeworks.all()
#
#     def perform_create(self, serializer):
#         """Метод предопределения автора."""
#         teacher = get_object_or_404(Teacher,
#                                     user=self.request.user)
#         serializer.save(teacher=teacher)
#
#
# class HomeworkStudentViewSet(ReadOnlyModelViewSet):
#     """ViewSet для эндпойнта /homework_students/
#     c пагинацией"""
#
#     serializer_class = HomeworkStudentSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = HomeworkFilter
#
#     def get_queryset(self):
#         """Метод обработки запроса."""
#         return Homework.objects.filter(
#             teacher__lessons__teacherstudent__email=self.request.user.email)


class TeacherLessonViewSet(ModelViewSet):
    """
    ViewSet для эндпойнта /lessons_teachers/
    c пагинацией и кастомной фильтрацией
    """

    serializer_class = LessonSerializer
    http_method_names = ['get', 'patch', 'post', 'delete']
    filterset_class = LessonFilter

    def get_permissions(self):
        if self.action in ('get', 'patch', 'delete'):
            return [IsAuthenticated(), IsTeacherOwner()]
        return [IsTeacher()]

    def get_queryset(self):
        """Получения queryset уроков учителя"""
        teacher = get_object_or_404(Teacher,
                                    user=self.request.user)
        return teacher.lessons.all()

    def perform_create(self, serializer):
        """Метод создания учителя у урока."""
        teacher = get_object_or_404(Teacher,
                                    user=self.request.user)
        serializer.save(teacher=teacher)


class StudentLessonViewSet(ReadOnlyModelViewSet):
    """ViewSet для эндпойнта /lessons_students/
    c пагинацией"""

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Метод обработки запроса."""
        return Lesson.objects.filter(
            teacher_student__email=self.request.user.email)
