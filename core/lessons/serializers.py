from datetime import date

from clients.models import Teacher
from django.shortcuts import get_object_or_404
from rest_framework.serializers import (
    CurrentUserDefault, ModelSerializer,
    SerializerMethodField, SlugRelatedField,
    ValidationError, StringRelatedField,
    PrimaryKeyRelatedField, BooleanField,
    ReadOnlyField)

from .models import Homework, Lesson


class HomeworkTeacherSerializer(ModelSerializer):
    """Сериализатор для представления ДЗ для учителя"""
    teacher = SlugRelatedField(slug_field='pk',
                               default=CurrentUserDefault(),
                               read_only=True)

    class Meta:
        model = Homework
        fields = ('id', 'teacher', 'title', 'text', 'comment')


class HomeworkStudentSerializer(ModelSerializer):
    """Сериализатор для представления ДЗ для студента"""
    teacher = SlugRelatedField(slug_field='pk',
                               read_only=True)

    class Meta:
        model = Homework
        fields = ('id', 'teacher', 'title', 'text', 'comment')


class SubjectPrimaryKeyRelated(PrimaryKeyRelatedField):
    """Возможность при создании урока выбора
     предмета урока только из предметов учителя"""
    def get_queryset(self):
        request = self.context.get('request', None)
        teacher = get_object_or_404(Teacher, user=request.user)
        return teacher.subjects.all()


class TeacherStudentPrimaryKeyRelated(PrimaryKeyRelatedField):
    """Возможность при создании урока выбора
    студента только из студентов учителя"""
    def get_queryset(self):
        request = self.context.get('request', None)
        teacher = get_object_or_404(Teacher, user=request.user)
        return teacher.studentM2M.all()


class HomeworkSlugRelated(SlugRelatedField):
    """Возможность при создании урока
     выбора ДЗ только из ДЗ учителя"""
    def get_queryset(self):
        request = self.context.get('request', None)
        teacher = get_object_or_404(Teacher, user=request.user)
        return teacher.homeworks.all()


class AbstractLessonSerializer(ModelSerializer):
    status = ReadOnlyField()
    homework = BooleanField(read_only=True)

    class Meta:
        model = Lesson
        fields = ['id',
                  'date',
                  'start_time',
                  'end_time',
                  'status',
                  'homework',
                  ]
        ordering = ['date', 'start_time']


class TeacherListLessonSerializer(AbstractLessonSerializer):
    """Сериализатор для представления списка уроков для учителя"""
    student_full_name = SerializerMethodField(read_only=True)
    student = TeacherStudentPrimaryKeyRelated(source='teacher_student',
                                              write_only=True)
    subject = SubjectPrimaryKeyRelated(write_only=True)

    def get_student_full_name(self, obj):
        return f"{obj.teacher_student.last_name} {obj.teacher_student.first_name}"

    class Meta(AbstractLessonSerializer.Meta):
        fields = AbstractLessonSerializer.Meta.fields + ['student_full_name', 'student', 'subject']


class StudentListLessonSerializer(AbstractLessonSerializer):
    """Сериализатор для представления списка уроков для ученика"""
    teacher = StringRelatedField(read_only=True)

    class Meta(AbstractLessonSerializer.Meta):
        fields = AbstractLessonSerializer.Meta.fields + ['teacher']


class TeacherDetailLessonSerializer(AbstractLessonSerializer):
    """
    Сериализатор для представления конкретного урока учителю,
    он имеет возможность также удалять и редактировать урок
    """
    student = TeacherStudentPrimaryKeyRelated(source='teacher_student',
                                              write_only=True)
    student_full_name = SerializerMethodField(read_only=True)
    subject = SubjectPrimaryKeyRelated(write_only=True)
    subject_title = StringRelatedField(source='subject',
                                       read_only=True)

    def get_student_full_name(self, obj):
        return f"{obj.teacher_student.last_name} {obj.teacher_student.first_name}"

    def validate(self, data):
        """
        Валидация даты и времени урока
        (проверка время окончание урока позже времени начала урока,
         дата урока не раньше сегодня)
        """
        if data['start_time'] > data['end_time']:
            raise ValidationError(
                'Время окончание урока должно'
                ' быть позже времени начала урока!')
        if data['date'] < date.today():
            raise ValidationError(
                'Урок не может быть раньше сегодняшней даты!')
        return data

    def update(self, instance, validated_data):
        teacher = validated_data.get('teacher', None)
        student = validated_data.get('student', None)
        if teacher or student:
            raise ValidationError("Нельзя изменить участников урока!")
        return super().update(instance, validated_data)

    class Meta(AbstractLessonSerializer.Meta):
        fields = AbstractLessonSerializer.Meta.fields + ['student', 'student_full_name',
                                                         'subject', 'subject_title',
                                                         'topic', 'comment']


class StudentDetailLessonSerializer(AbstractLessonSerializer):
    """Сериализатор для представления конкретного урока ученику"""
    teacher = StringRelatedField(read_only=True)
    subject_title = StringRelatedField(source='subject',
                                       read_only=True)

    class Meta(AbstractLessonSerializer.Meta):
        fields = AbstractLessonSerializer.Meta.fields + ['teacher', 'subject_title',
                                                         'topic', 'comment']
