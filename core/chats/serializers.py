from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    StringRelatedField,
)

from common.serializers import (
    SubjectPrimaryKeyRelated,
    TeacherPrimaryKeyRelated,
    TeacherStudentPrimaryKeyRelated
)
from .models import Homework, Message


class TeacherHomeworkSerializer(ModelSerializer):
    """
    Сериализатор обработки ДЗ для репетитора
    """
    subject = SubjectPrimaryKeyRelated(write_only=True, allow_null=True)
    subject_title = StringRelatedField(source="subject", read_only=True)
    student = TeacherStudentPrimaryKeyRelated(source="teacher_student", write_only=True)
    student_full_name = SerializerMethodField(read_only=True)

    def get_student_full_name(self, obj):
        return f"{obj.teacher_student.last_name} {obj.teacher_student.first_name}"

    class Meta:
        model = Homework
        fields = (
            "id",
            "student",
            "student_full_name",
            "timestamp",
            "subject",
            "subject_title",
            "text",
            "file",
            "reply_file",
            "status",
        )
        read_only_fields = ("id", "reply_file", "timestamp")


class StudentHomeworkSerializer(ModelSerializer):
    """
    Сериализатор обработки ДЗ для ученика
    """
    subject = StringRelatedField(read_only=True)
    teacher = StringRelatedField(read_only=True)

    class Meta:
        model = Homework
        fields = (
            "id",
            "teacher",
            "timestamp",
            "subject",
            "text",
            "file",
            "reply_file",
            "status",
        )
        read_only_fields = (
            "id",
            "text",
            "file",
            "timestamp",
        )


class TeacherMessageSerializer(ModelSerializer):
    """
    Сериализатор обработки сообщений для репетитора
    """
    student = TeacherStudentPrimaryKeyRelated(source="teacher_student", write_only=True)

    class Meta:
        model = Message
        fields = (
            "id",
            "student",
            "sender",
            "timestamp",
            "text",
            "file",
        )
        read_only_fields = ("sender", "timestamp", )


class StudentMessageSerializer(ModelSerializer):
    """
    Сериализатор обработки сообщений для ученика
    """
    teacher = TeacherPrimaryKeyRelated(source="teacher_student", write_only=True)

    def get_student_full_name(self, obj):
        return f"{obj.teacher_student.last_name} {obj.teacher_student.first_name}"

    class Meta:
        model = Message
        fields = (
            "id",
            "teacher",
            "sender",
            "timestamp",
            "text",
            "file",
        )
        read_only_fields = ("sender", "timestamp",)
