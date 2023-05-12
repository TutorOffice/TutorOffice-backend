from clients.models import Teacher, Student
from clients.permissions import IsTeacherOwner, IsStudentOwner
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import (
    ModelViewSet,
    ReadOnlyModelViewSet
)

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
    http_method_names = ['get', 'patch', 'post', 'delete']
    filterset_class = MaterialFilter
    permission_classes = (IsAuthenticated, IsTeacherOwner)

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


class StudentMaterialViewSet(ReadOnlyModelViewSet):
    """
    ViewSet для работы с материалами ученика.
    Ученик может только просматривать материалы.
    """

    serializer_class = StudentMaterialSerializer
    http_method_names = ['get']
    filterset_class = MaterialFilter
    permission_classes = (IsAuthenticated, IsStudentOwner,)

    def get_queryset(self):
        """Получения queryset материалов  учителя"""
        student = get_object_or_404(Student,
                                    user=self.request.user)
        return Material.objects.filter(teacher_student__student=student)
