from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from common.permissions import IsTeacherOwner, IsStudentOwner

from .models import Homework, Message
from .permissions import IsSender
from .serializers import (
    StudentHomeworkSerializer,
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
    # filterset
    # pagination
    # select_related
    # изменить timestamp

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
    http_method_names = ("get", "patch",)
    serializer_class = StudentHomeworkSerializer
    permission_classes = (IsAuthenticated, IsStudentOwner)
    # filterset
    # pagination
    # select_related
    # изменить timestamp

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
    # filterset
    # pagination
    # select_related
    # изменить timestamp

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
    # serializer_class = StudentMessageSerializer

    def get_permissions(self):
        if self.action in ("partial_update", "destroy"):
            return [IsAuthenticated(), IsStudentOwner(), IsSender()]
        return [IsAuthenticated(), IsStudentOwner()]
    # filterset
    # pagination
    # select_related
    # указание teacher_student, который отправляет и student, который принимает сообщения

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(
            teacher_student__student=user.student_profile
        )

    # def perform_create(self, serializer):
    #     student = self.request.user.teacher_profile
    #     serializer.save(teacher=teacher)
