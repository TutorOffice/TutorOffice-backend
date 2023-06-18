from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    StringRelatedField
)

from common.serializers import (
    SubjectPrimaryKeyRelated,
    TeacherPrimaryKeyRelated,
    TeacherStudentPrimaryKeyRelated
)
from .models import Homework, Message, TeacherStudent


class TeacherHomeworkSerializer(ModelSerializer):
    """
    Сериализатор обработки ДЗ для репетитора
    """
    subject = SubjectPrimaryKeyRelated(write_only=True, allow_null=True)
    subject_title = StringRelatedField(source="subject", read_only=True)
    student = TeacherStudentPrimaryKeyRelated(source="teacher_student", write_only=True)
    student_full_name = SerializerMethodField(read_only=True)
    student_photo = SerializerMethodField(read_only=True, allow_null=True)

    def get_student_full_name(self, obj):
        return f"{obj.teacher_student.last_name} {obj.teacher_student.first_name}"

    def get_student_photo(self, obj):
        try:
            photo = obj.teacher_student.student.user.photo
            return photo or None
        except AttributeError:
            return None

    class Meta:
        model = Homework
        fields = (
            "id",
            "student",
            "student_full_name",
            "student_photo",
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
    teacher_photo = SerializerMethodField(read_only=True, allow_null=True)

    def get_teacher_photo(self, obj):
        photo = obj.teacher.user.photo
        return photo or None

    class Meta:
        model = Homework
        fields = (
            "id",
            "teacher",
            "teacher_photo",
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
    student_full_name = SerializerMethodField(read_only=True)
    teacher = StringRelatedField(read_only=True)
    sender_photo = SerializerMethodField(read_only=True, allow_null=True)

    def get_student_full_name(self, obj):
        return f"{obj.teacher_student.last_name} {obj.teacher_student.first_name}"

    def get_sender_photo(self, obj):
        if obj.sender == "teacher":
            photo = obj.teacher.user.photo
            return photo or None
        photo = obj.teacher_student.student.user.photo
        return photo or None

    class Meta:
        model = Message
        fields = (
            "id",
            "student",
            "student_full_name",
            "teacher",
            "sender",
            "sender_photo",
            "timestamp",
            "text",
            "file",
        )
        read_only_fields = ("id", "sender", "timestamp")


class StudentMessageSerializer(ModelSerializer):
    """
    Сериализатор обработки сообщений для ученика
    """
    teacher = TeacherPrimaryKeyRelated(
        write_only=True
    )
    student = StringRelatedField(
        source="teacher_student.student",
        read_only=True
    )
    sender_photo = SerializerMethodField(
        read_only=True,
        allow_null=True
    )
    teacher_full_name = StringRelatedField(
        source="teacher",
        read_only=True
    )

    def get_sender_photo(self, obj):
        request = self.context["request"]
        if self.context["view"].action == "create":
            photo = request.user.photo
            return photo or None
        if obj.sender == "teacher":
            photo = obj.teacher.user.photo
            return photo or None
        photo = obj.teacher_student.student.user.photo
        return photo or None

    class Meta:
        model = Message
        fields = (
            "id",
            "teacher",
            "teacher_full_name",
            "student",
            "sender",
            "sender_photo",
            "timestamp",
            "text",
            "file",
        )
        read_only_fields = ("id", "sender", "timestamp",)
