from rest_framework.serializers import (
    ChoiceField,
    DateField,
    ModelSerializer,
    SerializerMethodField,
    StringRelatedField,
    ValidationError,
    IntegerField,
    CharField,
)

from common.serializers import (
    SubjectPrimaryKeyRelated,
    TeacherStudentPrimaryKeyRelated,
)

from .models import TYPECHOICE, Material


class TeacherMaterialSerializer(ModelSerializer):
    """
    Сериализатор для материалов репетитора
    """

    subject = SubjectPrimaryKeyRelated(
        write_only=True,
        allow_null=True,
    )
    subject_title = StringRelatedField(source="subject")
    student = TeacherStudentPrimaryKeyRelated(
        source="teacher_student",
        write_only=True,
        many=True,
    )
    student_full_name = SerializerMethodField(
        read_only=True,
    )
    material_type = ChoiceField(
        choices=TYPECHOICE,
        default="private",
    )
    date = DateField(read_only=True)
    file_type = CharField(read_only=True)
    file_size = IntegerField(read_only=True)

    def get_student_full_name(self, obj):
        students = obj.teacher_student.all()
        return [
            f"{student.last_name} {student.first_name}" for student in students
        ]

    def validate(self, attrs):
        student = attrs.get("teacher_student", None)
        material_type = attrs.get("material_type", None)
        if student and material_type == "public":
            raise ValidationError(
                {"detail": "Нельзя указать ученика для публичного материала!"}
            )
        elif not student and material_type == "private":
            raise ValidationError(
                {
                    "detail": "Нельзя создать приватный материал "
                              "без указания ученика!"
                }
            )
        file = self.context["request"].FILES.get("file", None)
        if file:
            attrs["file_size"] = file.size // 1024
            attrs["file_type"] = file.content_type
        return attrs

    class Meta:
        model = Material
        fields = (
            "id",
            "student",
            "student_full_name",
            "subject",
            "subject_title",
            "file",
            "file_type",
            "file_size",
            "text",
            "material_type",
            "date",
        )

    def update(self, instance, validated_data):
        material_type = validated_data.get("material_type", None)
        if material_type == "public":
            instance.teacher_student.clear()
        return super().update(instance, validated_data)


class StudentMaterialSerializer(ModelSerializer):
    """
    Сериализатор для материалов ученика
    """

    subject = StringRelatedField()
    teacher = StringRelatedField()

    class Meta:
        model = Material
        fields = (
            "id",
            "teacher",
            "subject",
            "file",
            "file_type",
            "file_size",
            "text",
            "date",
        )
