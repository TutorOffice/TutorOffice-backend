from clients.models import Teacher, Student
from clients.services import get_user_type
from clients.permissions import IsTeacherOwner, IsStudentOwner, IsTeacher

from django.db.models import Count, F, Value, CharField
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ReadOnlyModelViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin
from rest_framework.response import Response

from .filters import LessonFilter, HomeworkFilter
from .models import Homework, Lesson
from .serializers import (HomeworkStudentSerializer, HomeworkTeacherSerializer,
                          TeacherListLessonSerializer, StudentListLessonSerializer,
                          TeacherDetailLessonSerializer, StudentDetailLessonSerializer)


class HomeworkTeacherViewSet(ModelViewSet):
    """ViewSet для эндпойнта /homeworks_teachers/
    c пагинацией и поиском по полю title"""

    serializer_class = HomeworkTeacherSerializer
    http_method_names = ['get', 'patch', 'post', 'delete']
    filterset_class = HomeworkFilter
    permission_classes = [IsAuthenticated,
                          IsTeacherOwner]

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
    filterset_class = HomeworkFilter

    def get_queryset(self):
        """Метод обработки запроса."""
        return Homework.objects.filter(
            teacher__lessons__teacherstudent__email=self.request.user.email)


class AggregateLessonsViewSet(ListModelMixin, GenericViewSet):
    """
    Вьюсет для возврата количества уроков
    с возможностью выбора параметров для
    фильтрации и группировки данных.
    """
    filterset_class = LessonFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Возвращаются все уроки для учителя и ученика,
        в зависимости от типа профиля это осуществляется по-разному,
        т.к. ученик напрямую не связан с уроками
        """
        request = self.request
        profile = get_user_type(request)
        if profile == 'teacher':
            teacher = get_object_or_404(Teacher,
                                        user=self.request.user)
            return teacher.lessons.all()
        student = get_object_or_404(Student,
                                    user=self.request.user)
        return Lesson.objects.filter(teacher_student__student=student)

    def list(self, request, *args, **kwargs):
        """
        Отфильтрованные данные группируются по выбранному параметру,
        по умолчанию это дата, но также имеется возможность по
        предметам, учителям для учеников и ученикам для учителей.
        """
        queryset = self.filter_queryset(self.get_queryset())
        group_by = request.query_params.get('group_by', None)
        match group_by:
            # добавить поле status в values
            case 'subject':
                lessons = queryset.values(title=F('subject__title')).annotate(count=Count('id'))
            case 'status':
                lessons = queryset.values('status').annotate(count=Count('id'))
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


class ListLessonViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    """
    Возвращает список уроков с пагинацией и
    возможностью фильтрации
    """

    permission_classes = [IsAuthenticated]
    filterset_class = LessonFilter

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsTeacher()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        request = self.request
        profile = get_user_type(request)
        if profile == 'teacher':
            return TeacherListLessonSerializer
        return StudentListLessonSerializer

    def get_queryset(self):
        request = self.request
        profile = get_user_type(request)
        if profile == 'teacher':
            teacher = get_object_or_404(Teacher,
                                        user=self.request.user)
            return teacher.lessons.all()
        student = get_object_or_404(Student,
                                    user=self.request.user)
        return Lesson.objects.filter(teacher_student__student=student)

    def perform_create(self, serializer):
        """Метод создания учителя у урока."""
        teacher = get_object_or_404(Teacher,
                                    user=self.request.user)
        serializer.save(teacher=teacher)


class DetailTeacherLessonViewSet(ModelViewSet):
    """
    Возвращает конкретный урок
    как для учителей, только учитель имеет право
    создавать, редактировать и удалять урок
    """

    http_method_names = ['get', 'patch', 'delete']
    serializer_class = TeacherDetailLessonSerializer
    permission_classes = [IsAuthenticated, IsTeacherOwner]
    queryset = Lesson.objects.all()


class DetailStudentLessonViewSet(RetrieveModelMixin, GenericViewSet):
    """
    Возвращает конкретный урок для ученика,
    имеется только возможность чтения
    """
    serializer_class = StudentDetailLessonSerializer
    permission_classes = [IsAuthenticated, IsStudentOwner]
    queryset = Lesson.objects.all()
