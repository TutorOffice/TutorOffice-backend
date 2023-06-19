from django.db import models
from django.db.models import Count


class AggregateHomeworkQueryset(models.QuerySet):
    """Кастомный Queryset для подсчёта ДЗ по статусу"""

    def count_by_status(self):
        """Подсчёт ДЗ юзера по статусам"""
        return self.values("status").annotate(count=Count("id"))


class AggregateLessonManager(models.Manager):
    """
    Кастомный менеджер для подсчёта ДЗ по статусу,
    использует новые методы, определенные в кастомном queryset
    """

    def get_queryset(self):
        """Возвращает экземпляр кастомного queryset'a"""
        return AggregateHomeworkQueryset(self.model)

    def count_by_status(self):
        return self.get_queryset().count_by_status()
