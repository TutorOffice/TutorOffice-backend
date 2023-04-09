from django_filters import CharFilter, ChoiceFilter, FilterSet

from .models import TYPECHOICE, Material


class MaterialFilter(FilterSet):
    """Фильтры по всем полям модели Lesson"""

    teacher_student = CharFilter(field_name='teacher_student__last_name',
                                 lookup_expr='iexact',
                                 label='Фамилия студента')
    subject = CharFilter(field_name='subject__title',
                         lookup_expr='iexact',
                         label='Предмет')
    text = CharFilter(field_name='text',
                      lookup_expr='icontains',
                      label='Встречается в тексте')
    type = ChoiceFilter(choices=TYPECHOICE,
                        label='Тип материала')

    class Meta:
        model = Material
        fields = ('teacher_student', 'subject', 'text', 'type')
