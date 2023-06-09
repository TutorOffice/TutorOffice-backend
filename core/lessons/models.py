from datetime import date

from clients.models import Subject, Teacher, TeacherStudent
from django.core.exceptions import ValidationError
from django.db import models
from lessons.managers import AggregateLessonManager

PLANNED = "planned"
CANCELED = "canceled"
DONE = "done"

STATUSCHOICE = [
    (PLANNED, "planned"),
    (CANCELED, "canceled"),
    (DONE, "done"),
]


class Lesson(models.Model):
    """Модель для занятий"""

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.PROTECT,
        verbose_name="Учитель",
        related_name="t_lessons",
    )
    teacher_student = models.ForeignKey(
        TeacherStudent,
        on_delete=models.PROTECT,
        verbose_name="Псевдоученик",
        related_name="ts_lessons",
    )
    date = models.DateField(verbose_name="Дата")
    start_time = models.TimeField(
        verbose_name="Начало урока",
    )
    end_time = models.TimeField(
        verbose_name="Конец урока",
    )
    subject = models.ForeignKey(
        Subject,
        null=True,
        on_delete=models.PROTECT,
        verbose_name="Предмет",
    )
    student_comment = models.TextField(
        blank=True,
        max_length=100,
        verbose_name="Комментарий ученика",
    )
    teacher_comment = models.TextField(
        blank=True,
        max_length=100,
        verbose_name="Комментарий репетитора",
    )
    status = models.CharField(
        choices=STATUSCHOICE,
        default=PLANNED,
        verbose_name="Статус",
        max_length=10,
    )

    def __str__(self):
        return f"{self.teacher_student}"

    def clean(self):
        """Валидация даты и времени урока"""
        errors = {}
        if self.end_time <= self.start_time:
            errors["end_time"] = ValidationError(
                "Время конца урока должно быть позже времени начала урока!"
            )
        if self.date < date.today():
            errors["date"] = ValidationError(
                "Дата урока не может быть раньше текущего дня!"
            )
        if errors:
            raise ValidationError(errors)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ("teacher", "date", "subject", "start_time")

    objects = AggregateLessonManager()
