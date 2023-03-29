from clients.models import Teacher
from clients.permissions import IsTeacherOwnerOrIsStaffPermission
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .serializers import MaterialSerializer


class MaterialViewSet(ModelViewSet):
    """ViewSet для эндпойнта /materials/"""

    serializer_class = MaterialSerializer
    http_method_names = ['get', 'patch', 'post', 'delete']
#   pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated, IsTeacherOwnerOrIsStaffPermission]

    def get_queryset(self):
        """Получения queryset материалов  учителя"""
        teacher = get_object_or_404(Teacher,
                                    user=self.request.user)
        return teacher.materials.all()

    def perform_create(self, serializer):
        """Метод создания автора."""
        teacher = get_object_or_404(Teacher,
                                    user=self.request.user)
        serializer.save(teacher=teacher)
