import uuid

from django.db import models
from clients.models import TeacherStudent, Teacher, Subject

from .managers import AggregateLessonManager

SENDED = "sended"
DONE = "done"
ACCEPTED = "accepted"

STATUSCHOICE = [
    (SENDED, "sended"),
    (ACCEPTED, "accepted"),
    (DONE, "done"),
]


class Homework(models.Model):
    """Модель ДЗ"""
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.PROTECT,
        verbose_name="Учитель",
        related_name="t_homeworks",
    )
    teacher_student = models.ForeignKey(
        TeacherStudent,
        on_delete=models.PROTECT,
        verbose_name="Псевдоученик",
        related_name="ts_homeworks",
    )
    timestamp = models.DateTimeField(
        verbose_name="Дата и время",
        auto_now_add=True,
    )
    subject = models.ForeignKey(
        Subject,
        null=True,
        on_delete=models.PROTECT,
        verbose_name="Предмет",
    )
    text = models.TextField(
        verbose_name="Текст",
        blank=True,
    )
    file = models.FileField(
        verbose_name="Файл",
        upload_to="homeworks/tasks",
    )
    reply_file = models.FileField(
        verbose_name="Ответный файл",
        upload_to="homeworks/replies",
        null=True,
    )
    status = models.CharField(
        verbose_name="Статус",
        max_length=10,
        choices=STATUSCHOICE,
        default=SENDED,
    )

    objects = AggregateLessonManager()


class Message(models.Model):
    """Модель сообщений"""
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.PROTECT,
        verbose_name="Учитель",
        related_name="t_messages",
    )
    teacher_student = models.ForeignKey(
        TeacherStudent,
        on_delete=models.PROTECT,
        verbose_name="Псевдоученик",
        related_name="ts_messages",
    )
    timestamp = models.DateTimeField(
        verbose_name="Дата и время",
        auto_now_add=True,
    )
    text = models.TextField(
        verbose_name="Текст",
    )
    file = models.FileField(
        verbose_name="Файл",
        upload_to="messages/",
        null=True,
    )
    sender = models.CharField(
        verbose_name="Отправитель",
        max_length=256,
    )
