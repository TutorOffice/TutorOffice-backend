from clients.models import Teacher
from clients.permissions import IsTeacherOwner, IsTeacher

from django.db.models import Count, F, Value, CharField
from django.db.models.functions import Concat

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from .filters import LessonFilter # HomeworkFilter,
from .models import Homework, Lesson
from .serializers import (HomeworkStudentSerializer, HomeworkTeacherSerializer,
                          LessonSerializer, AggregateLessonSerializer)


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


class AggregateLessonsViewSet(ListModelMixin, GenericViewSet):
    """
    Вьюсет для возврата агрегированных данных по урокам
    с возможностью фильтрации
    """
    filterset_class = LessonFilter
    permission_classes = [IsAuthenticated]
    serializer_class = AggregateLessonSerializer

    def get_queryset(self):
        try:
            profile = self.request.user.teacher_profile
        except Teacher.DoesNotExist:
            profile = None
        if profile:
            teacher = get_object_or_404(Teacher,
                                        user=self.request.user)
            return teacher.lessons.all()
        return Lesson.objects.filter(
            teacher_student__email=self.request.user.email)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)
        group_by = request.query_params.get('group_by', None)
        match group_by:
            # добавить поле status в values
            case 'subject':
                lessons = queryset.values(title=F('subject__title')).annotate(count=Count('id'))
            case 'teacher':
                lessons = queryset.values(
                    full_name=Concat(
                        F('teacher__user__last_name'),
                        Value(' '),
                        F('teacher__user__first_name'),
                        output_field=CharField())).annotate(count=Count('id'))
            case 'student':
                lessons = queryset.values(
                    full_name=Concat(
                        F('teacher_student__last_name'),
                        Value(' '),
                        F('teacher_student__first_name'),
                        output_field=CharField())).annotate(count=Count('id'))
            case _:
                lessons = queryset.values('date').annotate(count=Count('id'))
        return Response({'lessons': lessons})


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
