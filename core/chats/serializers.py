from django.shortcuts import get_object_or_404
from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField,
    SerializerMethodField,
    StringRelatedField,
)

from clients.models import Teacher
from .models import Homework


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


class TeacherHomeworkSerializer(ModelSerializer):
    subject = SubjectPrimaryKeyRelated(write_only=True, allow_null=True)
    subject_title = StringRelatedField(source="subject", read_only=True)
    student = TeacherStudentPrimaryKeyRelated(source="teacher_student", write_only=True)
    teacher_student = SerializerMethodField(read_only=True)

    def get_teacher_student(self, obj):
        return f"{obj.teacher_student.last_name} {obj.teacher_student.first_name}"

    class Meta:
        model = Homework
        fields = (
            "id",
            "student",
            "teacher_student",
            "timestamp",
            "subject",
            "subject_title",
            "text",
            "file",
            "reply_file",
            "status",
        )
        read_only_fields = ("id", "reply_file", "timestamp")
