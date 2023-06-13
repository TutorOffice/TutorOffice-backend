# Generated by Django 4.2.1 on 2023-06-13 20:45

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("clients", "0013_alter_teacherstudent_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "timestamp",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата и время"
                    ),
                ),
                ("text", models.TextField(verbose_name="Текст")),
                (
                    "file",
                    models.FileField(
                        null=True, upload_to="messages/", verbose_name="Файл"
                    ),
                ),
                (
                    "teacher",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="t_messages",
                        to="clients.teacher",
                        verbose_name="Учитель",
                    ),
                ),
                (
                    "teacher_Student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="ts_messages",
                        to="clients.teacherstudent",
                        verbose_name="Псевдоученик",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Homework",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "timestamp",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата и время"
                    ),
                ),
                ("text", models.TextField(blank=True, verbose_name="Текст")),
                (
                    "file",
                    models.FileField(
                        upload_to="homeworks/tasks", verbose_name="Файл"
                    ),
                ),
                (
                    "reply_file",
                    models.FileField(
                        null=True,
                        upload_to="homeworks/replies",
                        verbose_name="Ответный файл",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("sended", "sended"),
                            ("accepted", "accepted"),
                            ("done", "done"),
                        ],
                        default="sended",
                        max_length=10,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "subject",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="clients.subject",
                        verbose_name="Предмет",
                    ),
                ),
                (
                    "teacher",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="t_homeworks",
                        to="clients.teacher",
                        verbose_name="Учитель",
                    ),
                ),
                (
                    "teacher_Student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="ts_homeworks",
                        to="clients.teacherstudent",
                        verbose_name="Псевдоученик",
                    ),
                ),
            ],
        ),
    ]
