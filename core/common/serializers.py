from django.shortcuts import get_object_or_404

from rest_framework.serializers import PrimaryKeyRelatedField

from clients.models import Teacher


class SubjectPrimaryKeyRelated(PrimaryKeyRelatedField):
    """
    Возможность выбора предмета
    только из предметов учителя
    """

    def get_queryset(self):
        request = self.context.get("request", None)
        teacher = get_object_or_404(Teacher, user=request.user)
        return teacher.subjects.all()


class TeacherStudentPrimaryKeyRelated(PrimaryKeyRelatedField):
    """
    Возможность выбора ученика
    только из учеников преподавателя
    """

    def get_queryset(self):
        request = self.context.get("request", None)
        teacher = get_object_or_404(Teacher, user=request.user)
        return teacher.studentM2M.all()


class TeacherPrimaryKeyRelated(PrimaryKeyRelatedField):
    """
    Возможность выбора преподавателя
    только из преподавателей ученика
    """
    def get_queryset(self):
        request = self.context.get("request", None)
        return Teacher.objects.filter(
            studentM2M__student=request.user.student_profile
        )