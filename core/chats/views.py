from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from clients.models import TeacherStudent
from common.permissions import IsTeacherOwner, IsStudentOwner
from clients.services import get_user_type

from .filters import HomeworkFilter, MessageFilter
from .models import Homework, Message
from .permissions import IsSender
from .serializers import (
    StudentHomeworkSerializer,
    StudentMessageSerializer,
    TeacherHomeworkSerializer,
    TeacherMessageSerializer,
)


class TeacherHomeworkViewSet(ModelViewSet):
    """
    ViewSet для работы с ДЗ
    для репетитора, репетитор имеет
    возможность создавать, удалять
    и изменять ДЗ.
    """
    http_method_names = ("get", "post", "patch", "delete")
    serializer_class = TeacherHomeworkSerializer
    permission_classes = (IsAuthenticated, IsTeacherOwner)
    filterset_class = HomeworkFilter

    def get_queryset(self):
        user = self.request.user
        return Homework.objects.filter(teacher__user=user)

    def perform_create(self, serializer):
        teacher = self.request.user.teacher_profile
        serializer.save(teacher=teacher, status="sended")


class StudentHomeworkViewSet(ModelViewSet):
    """
    ViewSet для работы с ДЗ
    для ученика, ученик имеет
    возможность создавать, удалять
    и изменять статус ДЗ.
    """
    http_method_names = ("get", "patch")
    serializer_class = StudentHomeworkSerializer
    permission_classes = (IsAuthenticated, IsStudentOwner)
    filterset_class = HomeworkFilter

    def get_queryset(self):
        user = self.request.user
        return Homework.objects.filter(teacher_student__student=user.student_profile)


class TeacherMessageViewSet(ModelViewSet):
    """
    ViewSet для обработки сообщений
    для репетитора
    """
    http_method_names = ("get", "post", "patch", "delete")
    serializer_class = TeacherMessageSerializer
    filterset_class = MessageFilter

    def get_permissions(self):
        if self.action in ("partial_update", "destroy"):
            return [IsAuthenticated(), IsTeacherOwner(), IsSender()]
        return [IsAuthenticated(), IsTeacherOwner()]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(teacher__user=user)

    def perform_create(self, serializer):
        teacher = self.request.user.teacher_profile
        serializer.save(teacher=teacher, sender="teacher")


class StudentMessageViewSet(ModelViewSet):
    """
    ViewSet для обработки сообщений
    для ученика
    """
    http_method_names = ("get", "post", "patch", "delete")
    serializer_class = StudentMessageSerializer
    filterset_class = MessageFilter

    def get_permissions(self):
        if self.action in ("partial_update", "destroy"):
            return [IsAuthenticated(), IsStudentOwner(), IsSender()]
        return [IsAuthenticated(), IsStudentOwner()]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(
            teacher_student__student=user.student_profile
        )

    def perform_create(self, serializer):
        student = self.request.user.student_profile
        teacher = self.request.data["teacher"]
        obj = TeacherStudent.objects.get(
            teacher=teacher, student=student
        )
        serializer.save(
            teacher_student=obj,
            sender="student"
        )


class AggregateHomeworks(ListModelMixin, GenericViewSet):
    """
    Вьюха для возврата количества ДЗ
    для пользователя с фильтрацией
    с группировкой по ученкам и статусам для репетитора,
    а также репетиторам и статусам для ученика
    """
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]
    filterset_class = HomeworkFilter
    # pagination
    # optimization

    def get_queryset(self):
        """
        Получение набора записей ДЗ в
        зависимости от типа пользователя
        """
        request = self.request
        profile = get_user_type(request)
        if profile == "teacher":
            return Homework.objects.filter(
                teacher=request.user.teacher_profile
            )
        return Homework.objects.filter(
            teacher_student__student=request.user.student_profile
        )

    def list(self, request, *args, **kwargs):
        """
        Набор записей ДЗ фильтруется, если был выбран фильтр,
        а затем производится подсчёт количества ДЗ с
        группировкой по ученикам и статусам для репетиторов,
        а также репетиторам и статусам для учеников
        """
        queryset = self.filter_queryset(self.get_queryset())
        request = self.request
        profile = get_user_type(request)
        if profile == "teacher":
            homeworks = queryset.count_by_student()
        else:
            homeworks = queryset.count_by_teacher()
        return Response({"homeworks": homeworks})
