from django_filters import CharFilter, DateFromToRangeFilter, FilterSet

from .models import Lesson


class LessonFilter(FilterSet):
    """Фильтры по всем полям модели Lesson"""

    teacher = CharFilter(
        # используется id юзера, а не учителя
        field_name="teacher__user__id",
        label="Репетитор",
    )
    student = CharFilter(
        field_name="teacher_student__id",
        label="Студент",
    )
    date = DateFromToRangeFilter(
        field_name="date",
        label="Дата",
    )
    subject = CharFilter(
        field_name="subject__id",
        label="Предмет",
    )

    class Meta:
        model = Lesson
        fields = (
            "teacher",
            "student",
            "date",
            "subject",
            "status",
        )
