"""Кастомный фильтр для представления Lesson.
    Фильтрация по фамилии студента, названию предмета,
    ключевым словам в заголовке домашней работы и диапазону дат.
"""
from django_filters import CharFilter, FilterSet, DateFromToRangeFilter
from .models import Lesson

class LessonFilter(FilterSet):
    """Фильтры по всем полям модели Lesson"""

    teacher_student = CharFilter(field_name='teacher_student__last_name', lookup_expr='exact')
    date = DateFromToRangeFilter(field_name='date')
    subject = CharFilter(field_name='subject__title', lookup_expr='exact')
    homework = CharFilter(field_name='homework__title', lookup_expr='contains')

    class Meta:
        model = Lesson
        fields = ('teacher_student', 'date', 'subject', 'homework')
