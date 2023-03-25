from rest_framework import serializers
from .models import Lesson, Homework
from clients.models import Subject, Teacher, TeacherStudent
from clients.serializers import SubjectSerializer
from rest_framework.serializers import (
    ModelSerializer,
    SlugRelatedField,
    CurrentUserDefault
)

class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = ('title', 'text', 'comment')

class LessonSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(read_only=True, many=True)
    teacher = SlugRelatedField(
        default=CurrentUserDefault(),
        read_only=True,
        slug_field="username",
    )
    teacher_student = SlugRelatedField(
        queryset=TeacherStudent.objects.all(), slug_field='teacher'
    )
    homework = HomeworkSerializer()

    class Meta:
        model = Lesson
        fields = ('teacher',
                  'teacher_student',
                  'subject',
                  'date',
                  'start_time',
                  'end_time',
                  'topic',
                  'comment',
                  'homework')

        ordering = ["-id"]


#class LessonCreateSerializer(serializers.ModelSerializer):
#    subject = SubjectSerializer(many=True, read_only=True)
#    teacher_student = SlugRelatedField(
#        queryset=TeacherStudent.objects.all(), slug_field='teacher'
#    )
##    homework = SlugRelatedField(slug_field='title', read_only=True)

  #  class Meta:
#        model = Lesson
  #      fields = ('teacher_student',
  ##                 'date',
  #                'start_time',
  #                'end_time',
 #                 'topic',
#                  'comment',
#                  'homework')
#
 #       ordering = ["-id"]
#