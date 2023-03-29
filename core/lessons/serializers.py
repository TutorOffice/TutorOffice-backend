from datetime import date
from .models import Lesson, Homework
from clients.models import Teacher
from django.shortcuts import get_object_or_404

from rest_framework.serializers import (
    ModelSerializer,
    SlugRelatedField,
    CurrentUserDefault,
    ValidationError
)


class HomeworkTeacherSerializer(ModelSerializer):
    """Сериализатор для представления ДЗ для учителя"""
    teacher = SlugRelatedField(slug_field='pk',
                               default=CurrentUserDefault(),
                               read_only=True)

    class Meta:
        model = Homework
        fields = ('teacher', 'title', 'text', 'comment')


class HomeworkStudentSerializer(ModelSerializer):
    """Сериализатор для представления ДЗ для студента"""
    teacher = SlugRelatedField(slug_field='pk',
                               read_only=True)

    class Meta:
        model = Homework
        fields = ('teacher', 'title', 'text', 'comment')


class SubjectSlugRelated(SlugRelatedField):
    """Возможность при создании урока выбора
     предмета урока только из предметов учителя"""
    def get_queryset(self):
        request = self.context.get('request', None)
        teacher = get_object_or_404(Teacher, user=request.user)
        return teacher.subjects.all()


class TeacherStudentSlugRelated(SlugRelatedField):
    """Возможность при создании урока выбора
    студента только из студентов учителя"""
    def get_queryset(self):
        request = self.context.get('request', None)
        teacher = get_object_or_404(Teacher, user=request.user)
        return teacher.teacherstudents.all()


class HomeworkSlugRelated(SlugRelatedField):
    """Возможность при создании урока
     выбора ДЗ только из ДЗ учителя"""
    def get_queryset(self):
        request = self.context.get('request', None)
        teacher = get_object_or_404(Teacher, user=request.user)
        return teacher.homeworks.all()


class LessonTeacherSerializer(ModelSerializer):
    """Сериализатор для представления уроков для учителя"""
    def validate(self, data):
        """
        Валидация даты и времени урока
        (проверка время окончание урока позже времени начала урока,
         дата урока не раньше сегодня)
        """
        if data['start_time'] > data['end_time']:
            raise ValidationError(
                'Время окончание урока должно быть позже времени начала урока!')
        if data['date'] < date.today():
            raise ValidationError(
                'Урок не может быть раньше сегодняшней даты!')
        return data

    subject = SubjectSlugRelated(slug_field='title')
    teacher = SlugRelatedField(slug_field='pk',
                               default=CurrentUserDefault(),
                               read_only=True)
    teacher_student = TeacherStudentSlugRelated(slug_field='last_name')
    homework = HomeworkSlugRelated(slug_field='title')

    class Meta:
        model = Lesson
        fields = ('id',
                  'teacher',
                  'teacher_student',
                  'subject',
                  'date',
                  'start_time',
                  'end_time',
                  'topic',
                  'comment',
                  'homework')

        ordering = ['date', 'start_time']


class LessonStudentSerializer(ModelSerializer):
    """Сериализатор для представления уроков для студента"""
    subject = SlugRelatedField(slug_field='title', read_only=True)
    teacher = SlugRelatedField(slug_field='pk',
                               read_only=True)
    teacher_student = SlugRelatedField(slug_field='last_name', read_only=True)
    homework = HomeworkStudentSerializer(read_only=True)

    class Meta:
        model = Lesson
        fields = ('id',
                  'teacher',
                  'teacher_student',
                  'subject',
                  'date',
                  'start_time',
                  'end_time',
                  'topic',
                  'comment',
                  'homework')

        ordering = ["teacher_student"]
