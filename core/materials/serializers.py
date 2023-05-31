from clients.models import Teacher
from django.shortcuts import get_object_or_404
from rest_framework.serializers import (
    ChoiceField,
    ModelSerializer, PrimaryKeyRelatedField,
    DateField, StringRelatedField, SerializerMethodField,
    ValidationError
)
from .models import TYPECHOICE, Material


class SubjectPrimaryKeyRelated(PrimaryKeyRelatedField):
    """
    Возможность при создании урока выбора
    предмета только из предметов учителя
    """
    def get_queryset(self):
        request = self.context.get('request', None)
        teacher = get_object_or_404(Teacher, user=request.user)
        return teacher.subjects.all()


class TeacherStudentPrimaryKeyRelated(PrimaryKeyRelatedField):
    """
    Возможность при создании урока выбора
    студента только из студентов учителя
    """
    def get_queryset(self):
        request = self.context.get('request', None)
        teacher = get_object_or_404(Teacher, user=request.user)
        return teacher.studentM2M.all()


class TeacherMaterialSerializer(ModelSerializer):
    """
    Сериализатор для материалов репетитора
    """
    subject = SubjectPrimaryKeyRelated(
       write_only=True,
       allow_null=True,
    )
    subject_title = StringRelatedField(
        source='subject'
    )
    student = TeacherStudentPrimaryKeyRelated(
        source='teacher_student',
        write_only=True,
        many=True,
    )
    student_full_name = SerializerMethodField(
        read_only=True,
    )
    type = ChoiceField(
        choices=TYPECHOICE,
        default='private',
    )
    date = DateField(
        read_only=True
    )

    def get_student_full_name(self, obj):
        students = obj.teacher_student.all()
        return [f"{student.last_name} {student.first_name}" for student in students]

    def validate(self, attrs):
        student = attrs.get('teacher_student', None)
        kind = attrs.get('type', None)
        if student and kind == 'public':
            raise ValidationError({
                "detail": "Нельзя указать ученика "
                          "для публичного материала!"
            })
        elif not student and kind == 'private':
            raise ValidationError({
                "detail": "Нельзя создать приватный материал "
                          "без указания ученика!"
            })
        return attrs

    class Meta:
        model = Material
        fields = ('id',
                  'student',
                  'student_full_name',
                  'subject',
                  'subject_title',
                  'file',
                  'text',
                  'type',
                  'date',
                  )

    def update(self, instance, validated_data):
        kind = validated_data.get('type', None)
        if kind == 'public':
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
        fields = ('id',
                  'teacher',
                  'subject',
                  'file',
                  'text',
                  'date',
                  )
