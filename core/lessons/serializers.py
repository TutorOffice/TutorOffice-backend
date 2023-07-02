from datetime import date

from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    ReadOnlyField,
    SerializerMethodField,
    StringRelatedField,
    ValidationError,
)

from common.serializers import (
    SubjectPrimaryKeyRelated,
    TeacherStudentPrimaryKeyRelated,
)

from .models import Lesson


class AbstractLessonSerializer(ModelSerializer):
    """
    Сериализатор, содержащий общие данные по урокам,
    для наследования другими сериализаторами
    """

    status = ReadOnlyField()

    def validate(self, data):
        """
        Валидация даты и времени урока
        (проверка время окончание урока позже времени начала урока,
         дата урока не раньше сегодня)
        """
        if data["start_time"] > data["end_time"]:
            raise ValidationError(
                "Время окончание урока должно быть позже времени начала урока!"
            )
        if data["date"] < date.today():
            raise ValidationError(
                "Урок не может быть раньше сегодняшней даты!"
            )
        return data

    class Meta:
        model = Lesson
        fields = [
            "id",
            "date",
            "start_time",
            "end_time",
            "status",
        ]
        ordering = ["date", "start_time"]


class TeacherListLessonSerializer(AbstractLessonSerializer):
    """Сериализатор для представления списка уроков для учителя"""

    student_full_name = SerializerMethodField(read_only=True)
    student = TeacherStudentPrimaryKeyRelated(
        source="teacher_student", write_only=True
    )
    subject = SubjectPrimaryKeyRelated(write_only=True, allow_null=True)
    teacher_comment = CharField(
        source="comment", write_only=True, required=False
    )

    def get_student_full_name(self, obj):
        return (
            f"{obj.teacher_student.last_name} {obj.teacher_student.first_name}"
        )

    class Meta(AbstractLessonSerializer.Meta):
        fields = AbstractLessonSerializer.Meta.fields + [
            "student_full_name",
            "student",
            "subject",
            "teacher_comment",
        ]


class StudentListLessonSerializer(AbstractLessonSerializer):
    """Сериализатор для представления списка уроков для ученика"""

    teacher = StringRelatedField(read_only=True)

    class Meta(AbstractLessonSerializer.Meta):
        fields = AbstractLessonSerializer.Meta.fields + ["teacher"]


class TeacherDetailLessonSerializer(AbstractLessonSerializer):
    """
    Сериализатор для представления конкретного урока учителю,
    он имеет возможность также удалять и редактировать урок
    """

    student_full_name = SerializerMethodField(read_only=True)
    subject = SubjectPrimaryKeyRelated(write_only=True, allow_null=True)
    subject_title = StringRelatedField(source="subject", read_only=True)
    status = CharField()

    def get_student_full_name(self, obj):
        return (
            f"{obj.teacher_student.last_name} {obj.teacher_student.first_name}"
        )

    class Meta(AbstractLessonSerializer.Meta):
        fields = AbstractLessonSerializer.Meta.fields + [
            "student_full_name",
            "subject",
            "subject_title",
            "teacher_comment",
        ]


class StudentDetailLessonSerializer(AbstractLessonSerializer):
    """Сериализатор для представления конкретного урока ученику"""

    teacher = StringRelatedField(read_only=True)
    subject_title = StringRelatedField(source="subject", read_only=True)

    class Meta(AbstractLessonSerializer.Meta):
        fields = AbstractLessonSerializer.Meta.fields + [
            "teacher",
            "subject_title",
            "student_comment",
        ]
        read_only_fields = (
            'status',
            'start_time',
            'end_time',
            'date',
            'status',
            'id',
        )
