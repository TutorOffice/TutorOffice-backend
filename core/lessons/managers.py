from django.db import models
from django.db.models import Count, F, Value, CharField
from django.db.models.functions import Concat


class AggregateLessonQueryset(models.QuerySet):
    """
    Кастомный Queryset для подсчёта уроков по выбранному параметру
    """

    def count_by_subjects(self):
        """
        Подсчёт уроков юзера по предметам,
        по которым проводится конкретный урок
        """
        return self.values(title=F("subject__title")).annotate(count=Count("id"))

    def count_by_status(self):
        """Подсчёт уроков юзера по статусу урока"""
        return self.values("status").annotate(count=Count("id"))

    def count_by_date(self):
        """
        Подсчёт уроков юзера по датам их проведения,
        используется по умолчанию
        """
        return self.values("date").annotate(count=Count("id"))

    def count_by_students(self):
        """
        Подсчёт уроков репетитора
        по каждому ученику
        """
        return self.values(
            full_name=Concat(
                F("teacher_student__last_name"), Value(" "), F("teacher_student__first_name"), output_field=CharField()
            )
        ).annotate(count=Count("id"))

    def count_by_teachers(self):
        """
        Подсчёт уроков ученика
        по каждому репетитору
        """
        return self.values(
            full_name=Concat(
                F("teacher__user__last_name"), Value(" "), F("teacher__user__first_name"), output_field=CharField()
            )
        ).annotate(count=Count("id"))


class AggregateLessonManager(models.Manager):
    """
    Кастомный менеджер для подсчёта уроков по выбранному параметру,
    использует новые методы, определенные в кастомном queryset
    """

    def get_queryset(self):
        """Возвращает экземпляр кастомного queryset'a"""
        return AggregateLessonQueryset(self.model)

    def count_by_subjects(self):
        return self.get_queryset().count_by_subjects()

    def count_by_status(self):
        return self.get_queryset().count_by_status()

    def count_by_date(self):
        return self.get_queryset().count_by_date()

    def count_by_students(self):
        return self.get_queryset().count_by_students()

    def count_by_teachers(self):
        return self.get_queryset().count_by_teachers()
