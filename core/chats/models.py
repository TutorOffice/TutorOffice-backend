import uuid

from django.db import models
from clients.models import TeacherStudent, Teacher, Subject

SENDED = "sended"
DONE = "done"
ACCEPTED = "accepted"


STATUSCHOICE = [
    (SENDED, "sended"),
    (ACCEPTED, "accepted"),
    (DONE, "done"),
]


class Chat(models.Model):
    """Модель чатов"""
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.PROTECT,
        verbose_name="Репетитор",
        related_name="t_chats",
    )
    teacher_student = models.OneToOneField(
        TeacherStudent,
        on_delete=models.PROTECT,
        verbose_name="Псевдоученик",
        related_name="ts_chats",
    )


class Homework(models.Model):
    """Модель ДЗ"""
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
    )
    chat = models.ForeignKey(
        Chat,
        on_delete=models.PROTECT,
        verbose_name="Чат",
        related_name="homeworks",
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


class Message(models.Model):
    """Модель сообщений"""
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
    )
    chat = models.ForeignKey(
        Chat,
        on_delete=models.PROTECT,
        verbose_name="Чат",
        related_name="messages",
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
        upload_to="homeworks/tasks",
        null=True,
    )
