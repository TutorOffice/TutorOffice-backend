from django_filters import (
    CharFilter,
    ChoiceFilter,
    DateFromToRangeFilter,
)

from common.filters import CommonFilter

from .models import TYPECHOICE, Material


class MaterialFilter(CommonFilter):
    """Фильтры по всем полям модели Lesson"""

    type = ChoiceFilter(
        choices=TYPECHOICE,
        label="Тип материала",
    )
    date = DateFromToRangeFilter(
        field_name="date",
        label="Дата",
    )

    class Meta:
        model = Material
        fields = [
            "teacher",
            "student",
            "subject",
            "type",
            "date",
        ]
