# Generated by Django 4.1.6 on 2023-03-26 19:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "clients",
            "0002_alter_teacher_students_alter_teacher_subjects_and_more",
        ),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="teacherstudent",
            options={
                "ordering": ("teacher",),
                "verbose_name": "Учитель-Ученик",
                "verbose_name_plural": "Учитель-Ученики",
            },
        ),
        migrations.AlterField(
            model_name="teacherstudent",
            name="first_name",
            field=models.TextField(
                error_messages={"invalid": "Имя указанo некорректно"},
                validators=[
                    django.core.validators.RegexValidator(
                        regex="^([А-ЯЁ]{1}[а-яё]{1,49})|([A-Z]{1}[a-z]{1,49})$"
                    ),
                    django.core.validators.MinLengthValidator(2),
                    django.core.validators.MaxLengthValidator(50),
                ],
                verbose_name="Имя",
            ),
        ),
        migrations.AlterField(
            model_name="teacherstudent",
            name="last_name",
            field=models.TextField(
                error_messages={"invalid": "Фамилия указана некорректно"},
                validators=[
                    django.core.validators.RegexValidator(
                        regex="^([А-ЯЁ]{1}[а-яё]{1,49})|([A-Z]{1}[a-z]{1,49})$"
                    ),
                    django.core.validators.MinLengthValidator(2),
                    django.core.validators.MaxLengthValidator(50),
                ],
                verbose_name="Фамилия",
            ),
        ),
        migrations.AlterField(
            model_name="teacherstudent",
            name="patronymic_name",
            field=models.TextField(
                blank=True,
                error_messages={"invalid": "Отчество указанo некорректно"},
                validators=[
                    django.core.validators.RegexValidator(
                        regex="^([А-ЯЁ]{1}[а-яё]{1,49})|([A-Z]{1}[a-z]{1,49})$"
                    ),
                    django.core.validators.MinLengthValidator(2),
                    django.core.validators.MaxLengthValidator(50),
                ],
                verbose_name="Отчество",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.TextField(
                error_messages={"invalid": "Имя указанo некорректно"},
                validators=[
                    django.core.validators.RegexValidator(
                        regex="^([А-ЯЁ]{1}[а-яё]{1,49})|([A-Z]{1}[a-z]{1,49})$"
                    ),
                    django.core.validators.MinLengthValidator(2),
                    django.core.validators.MaxLengthValidator(50),
                ],
                verbose_name="Имя",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="last_name",
            field=models.TextField(
                error_messages={"invalid": "Фамилия указана некорректно"},
                validators=[
                    django.core.validators.RegexValidator(
                        regex="^([А-ЯЁ]{1}[а-яё]{1,49})|([A-Z]{1}[a-z]{1,49})$"
                    ),
                    django.core.validators.MinLengthValidator(2),
                    django.core.validators.MaxLengthValidator(50),
                ],
                verbose_name="Фамилия",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="patronymic_name",
            field=models.TextField(
                blank=True,
                error_messages={"invalid": "Отчество указанo некорректно"},
                validators=[
                    django.core.validators.RegexValidator(
                        regex="^([А-ЯЁ]{1}[а-яё]{1,49})|([A-Z]{1}[a-z]{1,49})$"
                    ),
                    django.core.validators.MinLengthValidator(2),
                    django.core.validators.MaxLengthValidator(50),
                ],
                verbose_name="Отчество",
            ),
        ),
    ]
