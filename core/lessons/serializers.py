from .models import Lesson, Homework
from clients.models import TeacherStudent, Teacher
from django.shortcuts import get_object_or_404

from rest_framework.serializers import (
    ModelSerializer,
    SlugRelatedField,
    CurrentUserDefault,
)

class HomeworkSerializer(ModelSerializer):
    class Meta:
        model = Homework
        fields = ('title', 'text', 'comment')


class SubjectSlugRelated(SlugRelatedField):
    def get_queryset(self):
        request = self.context.get('request', None)
        teacher = get_object_or_404(Teacher, user=request.user)
        return teacher.subjects.all()


class TeacherStudentSlugRelated(SlugRelatedField):
    def get_queryset(self):
        request = self.context.get('request', None)
        teacher = get_object_or_404(Teacher, user=request.user)
        return TeacherStudent.objects.filter(teacher=teacher)


class HomeworkSlugRelated(SlugRelatedField):
    def get_queryset(self):
        request = self.context.get('request', None)
        teacher = get_object_or_404(Teacher, user=request.user)
        return teacher.homeworks.all()


class LessonTeacherSerializer(ModelSerializer):
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
    subject = SlugRelatedField(slug_field='title', read_only=True)
    teacher = SlugRelatedField(slug_field='pk',
                               read_only=True)
    teacher_student = SlugRelatedField(slug_field='last_name', read_only=True)
    homework = HomeworkSerializer()

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