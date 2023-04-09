from clients.models import Teacher
from clients.permissions import IsTeacherOwnerOrIsStaffPermission
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import HomeworkFilter, LessonFilter
from .models import Homework, Lesson
from .serializers import (HomeworkStudentSerializer, HomeworkTeacherSerializer,
                          LessonStudentSerializer, LessonTeacherSerializer)


class HomeworkTeacherViewSet(ModelViewSet):
    """ViewSet для эндпойнта /homeworks_teachers/
    c пагинацией и поиском по полю title"""

    serializer_class = HomeworkTeacherSerializer
    http_method_names = ['get', 'patch', 'post', 'delete']
    filter_backends = [DjangoFilterBackend]
    filterset_class = HomeworkFilter
    permission_classes = [IsAuthenticated,
                          IsTeacherOwnerOrIsStaffPermission]

    def get_queryset(self):
        """Получения queryset домашних заданий  учителя"""
        teacher = get_object_or_404(Teacher,
                                    user=self.request.user)
        return teacher.homeworks.all()

    def perform_create(self, serializer):
        """Метод предопределения автора."""
        teacher = get_object_or_404(Teacher,
                                    user=self.request.user)
        serializer.save(teacher=teacher)


class HomeworkStudentViewSet(ReadOnlyModelViewSet):
    """ViewSet для эндпойнта /homework_students/
    c пагинацией"""

    serializer_class = HomeworkStudentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = HomeworkFilter

    def get_queryset(self):
        """Метод обработки запроса."""
        return Homework.objects.filter(
            teacher__lessons__teacherstudent__email=self.request.user.email)


class LessonTeacherViewSet(ModelViewSet):
    """ViewSet для эндпойнта /lessons_teachers/
    c пагинацией и кастомной фильтрацией"""

    serializer_class = LessonTeacherSerializer
    http_method_names = ['get', 'patch', 'post', 'delete']
    filter_backends = [DjangoFilterBackend]
    filterset_class = LessonFilter
    permission_classes = [IsAuthenticated,
                          IsTeacherOwnerOrIsStaffPermission]

    def get_queryset(self):
        """Получения queryset уроков  учителя"""
        teacher = get_object_or_404(Teacher,
                                    user=self.request.user)
        return teacher.lessons.all()

    def perform_create(self, serializer):
        """Метод создания учителя у урока."""
        teacher = get_object_or_404(Teacher,
                                    user=self.request.user)
        serializer.save(teacher=teacher)


class LessonStudentViewSet(ReadOnlyModelViewSet):
    """ViewSet для эндпойнта /lessons_students/
    c пагинацией"""

    serializer_class = LessonStudentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Метод обработки запроса."""
        return Lesson.objects.filter(
            teacher_student__email=self.request.user.email)
