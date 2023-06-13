from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from clients.permissions import IsTeacherOwner

from .models import Homework
from .serializers import (
    TeacherHomeworkSerializer,
)


class TeacherHomeworkViewSet(ModelViewSet):
    """
    ViewSet для выполнения работы с ДЗ
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
    # update - not reply or teacher or student

    def get_queryset(self):
        user = self.request.user
        return Homework.objects.filter(teacher__user=user)

    def perform_create(self, serializer):
        teacher = self.request.user.teacher_profile
        serializer.save(teacher=teacher, status="sended")
