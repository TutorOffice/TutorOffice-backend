from clients.models import Teacher
from django.shortcuts import get_object_or_404
from rest_framework.serializers import (ChoiceField, CurrentUserDefault,
                                        ModelSerializer, SlugRelatedField)

from .models import TYPECHOICE, Material


class SubjectSlugRelated(SlugRelatedField):
    """Возможность при создании урока выбора
     предмета только из предметов учителя"""
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


class MaterialSerializer(ModelSerializer):
    """Сериализатор для представления материалов"""
    teacher = SlugRelatedField(slug_field='pk',
                               default=CurrentUserDefault(),
                               read_only=True)
    subject = SubjectSlugRelated(slug_field='title')

    teacher_student = TeacherStudentSlugRelated(
        slug_field='last_name', many=True)
    type = ChoiceField(choices=TYPECHOICE, default='private')

    class Meta:
        model = Material
        fields = ('id',
                  'teacher',
                  'teacher_student',
                  'subject',
                  'file',
                  'text',
                  'type')
