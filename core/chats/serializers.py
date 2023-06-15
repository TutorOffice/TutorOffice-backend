from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    StringRelatedField,
)

from common.serializers import SubjectPrimaryKeyRelated, TeacherStudentPrimaryKeyRelated
from .models import Homework, Message


class TeacherHomeworkSerializer(ModelSerializer):
    """
    Сериализатор обработки ДЗ для репетитора
    """
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
    teacher_student = SerializerMethodField(read_only=True)

    def get_teacher_student(self, obj):
        return f"{obj.teacher_student.last_name} {obj.teacher_student.first_name}"

    class Meta:
        model = Message
        fields = (
            "id",
            "student",
            "teacher_student",
            "timestamp",
            "text",
            "file",
        )


class StudentMessageSerializer(ModelSerializer):
    """
    Сериализатор обработки сообщений для ученика
    """
    student = TeacherStudentPrimaryKeyRelated(source="teacher_student", write_only=True)
    teacher_student = SerializerMethodField(read_only=True)

    def get_teacher_student(self, obj):
        return f"{obj.teacher_student.last_name} {obj.teacher_student.first_name}"

    class Meta:
        model = Message
        fields = (
            "id",
            "student",
            "teacher_student",
            "timestamp",
            "text",
            "file",
        )
