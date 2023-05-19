from datetime import date
from clients.models import Subject, Teacher, TeacherStudent
from django.core.exceptions import ValidationError
from django.db import models

from lessons.managers import AggregateLessonManager

PLANNED = 'planned'
CANCELED = 'canceled'
DONE = 'done'

STATUSCHOICE = [
    (PLANNED, 'planned'),
    (CANCELED, 'canceled'),
    (DONE, 'done'),
    ]


class Lesson(models.Model):
    """Модель для занятий"""
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.PROTECT,
        verbose_name='Учитель',
        related_name='lessons')
    teacher_student = models.ForeignKey(
        TeacherStudent,
        on_delete=models.PROTECT,
        verbose_name='Учитель-Ученик',
        related_name='lessons')
    date = models.DateField(
        verbose_name='Дата')
    start_time = models.TimeField(
        verbose_name='Начало урока')
    end_time = models.TimeField(
        verbose_name='Конец урока')
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        verbose_name='Предмет')
    topic = models.TextField(
        max_length=40,
        blank=True,
        verbose_name='Тема урока')
    comment = models.TextField(
        blank=True,
        verbose_name='Комментарий')
    status = models.CharField(
        choices=STATUSCHOICE,
        default=PLANNED,
        verbose_name='Статус',
        max_length=10,
    )

    def __str__(self):
        return f'{self.teacher_student}'

    def clean(self):
        """Валидация даты и времени урока"""
        errors = {}
        if self.end_time <= self.start_time:
            errors['end_time'] = ValidationError(
                'Время конца урока должно быть позже времени начала урока!')
        if self.date < date.today():
            errors['date'] = ValidationError(
                'Дата урока не может быть раньше текущего дня!')
        if errors:
            raise ValidationError(errors)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('teacher', 'date', 'subject', 'start_time')

    objects = AggregateLessonManager()


class Homework(models.Model):
    """Модель, описывающая ДЗ к занятию"""
    title = models.TextField(
        verbose_name='Заголовок'
    )
    text = models.TextField(
        verbose_name='Текст задания'
    )
    comment = models.TextField(
        blank=True,
        verbose_name='Комментарий к домашнему заданию')
    lesson = models.OneToOneField(
        Lesson,
        related_name='homework',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Урок'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Домашнее задание'
        verbose_name_plural = 'Домашние задания'
        ordering = ('title',)
