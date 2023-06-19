from django_filters import DateFromToRangeFilter

from common.filters import CommonFilter

from .models import Lesson


class LessonFilter(CommonFilter):
    """Фильтры по всем полям модели Lesson"""

    date = DateFromToRangeFilter(
        field_name="date",
        label="Дата",
    )

    class Meta:
        model = Lesson
        fields = [
            "teacher",
            "student",
            "subject",
            "date",
            # "status",
        ]
