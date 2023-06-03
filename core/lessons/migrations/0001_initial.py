# Generated by Django 4.1.6 on 2023-04-09 16:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("clients", "0007_alter_student_options_alter_teacher_options_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Lesson",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField(verbose_name="Дата")),
                ("start_time", models.TimeField(verbose_name="Начало урока")),
                ("end_time", models.TimeField(verbose_name="Конец урока")),
                ("topic", models.TextField(blank=True, max_length=40, verbose_name="Тема урока")),
                ("comment", models.TextField(blank=True, verbose_name="Комментарий")),
                (
                    "subject",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="clients.subject", verbose_name="Предмет"
                    ),
                ),
                (
                    "teacher",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="lessons",
                        to="clients.teacher",
                        verbose_name="Учитель",
                    ),
                ),
                (
                    "teacher_student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="lessons",
                        to="clients.teacherstudent",
                        verbose_name="Учитель-Ученик",
                    ),
                ),
            ],
            options={
                "verbose_name": "Урок",
                "verbose_name_plural": "Уроки",
                "ordering": ("teacher", "date", "subject", "start_time"),
            },
        ),
        migrations.CreateModel(
            name="Homework",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.TextField(verbose_name="Заголовок")),
                ("text", models.TextField(verbose_name="Текст задания")),
                ("comment", models.TextField(blank=True, verbose_name="Комментарий к домашнему заданию")),
                (
                    "lesson",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="homework",
                        to="lessons.lesson",
                        verbose_name="Домашняя работа",
                    ),
                ),
            ],
            options={
                "verbose_name": "Домашнее задание",
                "verbose_name_plural": "Домашние задания",
                "ordering": ("title",),
            },
        ),
    ]
