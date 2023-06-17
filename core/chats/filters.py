from django_filters import CharFilter, ChoiceFilter

from common.filters import CommonFilter

from .models import Homework, Message, STATUSCHOICE


class HomeworkFilter(CommonFilter):
    """Фильтры для модели ДЗ"""
    status = ChoiceFilter(
        choices=STATUSCHOICE,
        label="Статус ДЗ",
    )
    text = CharFilter(
        field_name="text",
        lookup_expr="icontains",
        label="Встречается в тексте",
    )

    class Meta:
        model = Homework
        fields = [
            "teacher",
            "student",
            "subject",
            "status",
            "text",
        ]


class MessageFilter(CommonFilter):
    """Фильтры для модели сообщений"""
    text = CharFilter(
        field_name="text",
        lookup_expr="icontains",
        label="Встречается в тексте",
    )

    class Meta:
        model = Message
        fields = [
            "teacher",
            "student",
            "text",
        ]
