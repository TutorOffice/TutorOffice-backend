# Generated by Django 4.1.6 on 2023-03-29 18:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("clients", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Material",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        blank=True,
                        upload_to="static/materials/",
                        verbose_name="Файл материалов",
                    ),
                ),
                ("text", models.TextField(blank=True, verbose_name="Текст материалов")),
                (
                    "type",
                    models.CharField(
                        choices=[("public", "public"), ("private", "private")],
                        default="private",
                        max_length=10,
                        verbose_name="Тип материалов",
                    ),
                ),
                (
                    "subject",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="clients.subject",
                        verbose_name="Предмет",
                    ),
                ),
                (
                    "teacher",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="materials",
                        to="clients.teacher",
                        verbose_name="Учитель",
                    ),
                ),
                (
                    "teacher_student",
                    models.ManyToManyField(
                        related_name="materials",
                        to="clients.teacherstudent",
                        verbose_name="Учитель-Ученик",
                    ),
                ),
            ],
            options={
                "verbose_name": "Материал",
                "verbose_name_plural": "Материалы",
                "ordering": ("subject", "teacher"),
            },
        ),
    ]
