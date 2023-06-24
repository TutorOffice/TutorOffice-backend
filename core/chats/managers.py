from django.db import models
from django.db.models import Count, Value, F, CharField
from django.db.models.functions import Concat


class AggregateHomeworkQueryset(models.QuerySet):
    """Кастомный Queryset для подсчёта ДЗ по статусу"""

    def count_by_teacher(self):
        """
        Подсчитывает кол-во дз по статусам
        для каждого репетитора ученика
        """
        return self.values(
            "status",
            full_name=Concat(
                F("teacher__user__last_name"),
                Value(" "),
                F("teacher__user__first_name"),
                output_field=CharField(),
            )
        ).annotate(count=Count("id")).annotate(count=Count("id"))

    def count_by_student(self):
        """
        Подсчитывает кол-во дз по статусам
        для каждого ученика репетитора
        """
        return self.values(
            "status",
            full_name=Concat(
                F("teacher_student__last_name"),
                Value(" "),
                F("teacher_student__first_name"),
                output_field=CharField(),
            )
        ).annotate(count=Count("id")).annotate(count=Count("id"))


class AggregateLessonManager(models.Manager):
    """
    Кастомный менеджер для подсчёта ДЗ по статусу,
    использует новые методы, определенные в кастомном queryset
    """

    def get_queryset(self):
        """Возвращает экземпляр кастомного queryset'a"""
        return AggregateHomeworkQueryset(self.model)

    def count_by_student(self):
        return self.get_queryset().count_by_student()

    def count_by_teacher(self):
        return self.get_queryset().count_by_teacher()
