from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from clients.permissions import IsTeacherOwner
from clients.services import get_user_type

from .models import Chat
from .serializers import TeacherChatSerializer, StudentChatSerializer


class ChatViewSet(ModelViewSet):
    http_method_names = ("get", "delete",)

    def get_permissions(self):
        if self.action in ("create", "destroy"):
            return [IsAuthenticated(), IsTeacherOwner()]
        return [IsAuthenticated()]

    def get_queryset(self):
        profile = get_user_type(self.request)
        if profile == "teacher":
            return Chat.objects.select_related(
                'teacher_student', 'teacher__user').filter(
                teacher__user=self.request.user
            )
        return Chat.objects.select_related(
            'teacher', 'teacher__user'
        ).filter(
            teacher_student__student__user=self.request.user
        )

    def get_serializer_class(self):
        profile = get_user_type(self.request)
        if profile == "teacher":
            return TeacherChatSerializer
        return StudentChatSerializer

    def perform_create(self, serializer):
        teacher = self.request.user.teacher_profile
        serializer.save(teacher=teacher)