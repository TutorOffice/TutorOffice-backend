from django_filters import CharFilter, ChoiceFilter, FilterSet, DateFromToRangeFilter

from .models import TYPECHOICE, Material


class MaterialFilter(FilterSet):
    """Фильтры по всем полям модели Lesson"""

    student = CharFilter(
        field_name='teacher_student__id',
        label='Ученик',
    )
    teacher = CharFilter(
        field_name='teacher__user__id',
        label='Репетитор',
    )
    subject = CharFilter(
        field_name='subject__id',
        label='Предмет',
    )
    text = CharFilter(
        field_name='text',
        lookup_expr='icontains',
        label='Встречается в тексте',
    )
    type = ChoiceFilter(
        choices=TYPECHOICE,
        label='Тип материала',)
    date = DateFromToRangeFilter(
        field_name='date',
        label='Дата',
    )

    class Meta:
        model = Material
        fields = ('student', 'subject', 'text', 'type', 'date',)
