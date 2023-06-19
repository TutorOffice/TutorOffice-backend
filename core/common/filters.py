from django_filters import FilterSet, CharFilter


class CommonFilter(FilterSet):
    """Общий фильтр для наследования"""
    teacher = CharFilter(
        field_name="teacher__user__id",
        label="Репетитор",
    )
    student = CharFilter(
        field_name="teacher_student__id",
        label="Студент",
    )
    subject = CharFilter(
        field_name="subject__id",
        label="Предмет",
    )
