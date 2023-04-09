"""Кастомный фильтр для представления Lesson.
    Фильтрация по фамилии студента, названию предмета,
    ключевым словам в заголовке домашней работы и диапазону дат.
"""
from django_filters import CharFilter, DateFromToRangeFilter, FilterSet

from .models import Homework, Lesson


class LessonFilter(FilterSet):
    """Фильтры по всем полям модели Lesson"""

    teacher_student = CharFilter(field_name='teacher_student__last_name',
                                 lookup_expr='exact',
                                 label='Студент')
    date = DateFromToRangeFilter(field_name='date',
                                 label='Дата')
    subject = CharFilter(field_name='subject__title',
                         lookup_expr='iexact',
                         label='Предмет')
    homework = CharFilter(field_name='homework__title',
                          lookup_expr='icontains',
                          label='Домашняя работа')

    class Meta:
        model = Lesson
        fields = ('teacher_student', 'date', 'subject', 'homework')


class HomeworkFilter(FilterSet):
    """Фильтры по полям title и text модели Homework"""

    title = CharFilter(field_name='title',
                       lookup_expr='icontains',
                       label='Заголовок')

    text = CharFilter(field_name='text',
                      lookup_expr='icontains',
                      label='Поиск в тексте')

    class Meta:
        model = Homework
        fields = ('title', 'text')

