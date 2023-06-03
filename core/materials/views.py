from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from clients.pagination import MaterialsPagination
from clients.permissions import IsTeacherOwner, IsStudentMaterialOwner
from .models import Material
from .filters import MaterialFilter
from .serializers import (
    TeacherMaterialSerializer,
    StudentMaterialSerializer,
)


class TeacherMaterialViewSet(ModelViewSet):
    """
    ViewSet для работы с материалами репетитора.
    Репетитор имеет возможность создания,
    обновления и удаления материалов.
    """

    serializer_class = TeacherMaterialSerializer
    http_method_names = ["get", "patch", "post", "delete"]
    filterset_class = MaterialFilter
    pagination_class = MaterialsPagination
    permission_classes = (IsAuthenticated, IsTeacherOwner)

    def get_queryset(self):
        """Получения материалов учителя"""
        return (
            Material.objects.select_related("subject")
            .prefetch_related("teacher_student")
            .filter(teacher__user=self.request.user)
        )

    def perform_create(self, serializer):
        """Добавления автора-учителя к материалу"""
        user = self.request.user
        serializer.save(teacher=user.teacher_profile)


class StudentMaterialViewSet(ReadOnlyModelViewSet):
    """
    ViewSet для работы с материалами ученика.
    Ученик может только просматривать материалы.
    """

    serializer_class = StudentMaterialSerializer
    http_method_names = ["get"]
    filterset_class = MaterialFilter
    pagination_class = MaterialsPagination
    permission_classes = (
        IsAuthenticated,
        IsStudentMaterialOwner,
    )

    def get_queryset(self):
        """Получения queryset материалов учителя"""
        request = self.request
        return Material.objects.select_related("teacher__user", "subject", "teacher").filter(
            teacher_student__student__user=request.user
        )
