from django.shortcuts import get_object_or_404

from rest_framework.serializers import PrimaryKeyRelatedField

from clients.models import Teacher


class SubjectPrimaryKeyRelated(PrimaryKeyRelatedField):
    """
    Возможность при создании урока выбора
    предмета только из предметов учителя
    """

    def get_queryset(self):
        request = self.context.get("request", None)
        teacher = get_object_or_404(Teacher, user=request.user)
        return teacher.subjects.all()


class TeacherStudentPrimaryKeyRelated(PrimaryKeyRelatedField):
    """Возможность при создании урока выбора
    студента только из студентов учителя"""

    def get_queryset(self):
        request = self.context.get("request", None)
        teacher = get_object_or_404(Teacher, user=request.user)
        return teacher.studentM2M.all()
