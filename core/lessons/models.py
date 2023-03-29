from django.db import models
from clients.models import User, TeacherStudent, Subject, Teacher
from django.core.exceptions import ValidationError
from datetime import date


class Homework(models.Model):
    """Модель, описывающая ДЗ к занятию"""
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.PROTECT,
        verbose_name='Учитель',
        related_name='homeworks')
    title = models.TextField(
        verbose_name='Заголовок'
    )
    text = models.TextField(
        verbose_name='Текст задания'
    )
    comment = models.TextField(
        blank=True,
        verbose_name='Комментарий к домашнему заданию')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Домашнее задание'
        verbose_name_plural = 'Домашние задания'
        ordering = ('title',)


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
    homework = models.OneToOneField(
        Homework,
        related_name='lessons',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Домашняя работа'
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
        ordering = ('teacher', 'subject', 'start_time')
