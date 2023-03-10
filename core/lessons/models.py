from django.db import models
from clients.models import User, TeacherStudent, Subject, Teacher


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
        verbose_name='Учитель')
    teacher_student = models.ForeignKey(
        TeacherStudent,
        on_delete=models.PROTECT)
    date = models.DateField(verbose_name='Дата')
    start_time = models.TimeField(
        verbose_name='Начало урока')
    end_time = models.TimeField(
        verbose_name='Конец урока')
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        verbose_name='Предмет')
    topic = models.TextField(max_length=40, blank=True)
    comment = models.TextField(blank=True)
    homework = models.OneToOneField(
        Homework,
        related_name='lesson',
        on_delete=models.CASCADE,
        blank=True,
        verbose_name='Домашняя работа'
    )

    def __str__(self):
        return f'{self.teacher_student}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('teacher', 'subject', 'start_time')
