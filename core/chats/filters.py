from django_filters import CharFilter, FilterSet

from .models import Homework, Message


class HomeworkFilter(FilterSet):
    """
    Фильтры для ДЗ
    """
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
    status = CharFilter(
        label="Статус"
    )

    class Meta:
        model = Homework
        fields = (
            "teacher",
            "student",
            "subject",
            "status"
        )


class MessageFilter(FilterSet):
    """
    Фильтры для сообщений
    """
    teacher = CharFilter(
        field_name="teacher__user__id",
        label="Репетитор",
    )
    student = CharFilter(
        field_name="teacher_student__id",
        label="Студент",
    )

    class Meta:
        model = Message
        fields = (
            "teacher",
            "student",
        )
