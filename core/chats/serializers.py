from rest_framework.serializers import (
    ModelSerializer,
    PrimaryKeyRelatedField,
    SerializerMethodField,
    StringRelatedField,
)

from clients.models import TeacherStudent
from .models import Chat


class TeacherStudentPrimaryKeyRelated(PrimaryKeyRelatedField):
    """
    При создании чата можно выбрать только тех
    учеников, что принадлежат этому репетитору, но
    только тех, с которыми чат ещё не создан
    """

    def get_queryset(self):
        request = self.context.get("request", None)
        teacher = request.user.teacher_profile
        return TeacherStudent.objects.filter(
            teacher=teacher
        ).exclude(
            ts_chats__teacher=teacher
        )


class TeacherChatSerializer(ModelSerializer):
    student = TeacherStudentPrimaryKeyRelated(
        source="teacher_student",
        write_only=True
    )
    student_full_name = SerializerMethodField(read_only=True)

    def get_student_full_name(self, obj):
        return f"{obj.teacher_student.last_name} {obj.teacher_student.first_name}"

    class Meta:
        model = Chat
        fields = ("id", "student", "student_full_name",)


class StudentChatSerializer(ModelSerializer):
    teacher = StringRelatedField(read_only=True)

    class Meta:
        model = Chat
        fields = ("id", "teacher")
