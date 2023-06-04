# Generated by Django 4.2.1 on 2023-06-03 21:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("clients", "0010_alter_user_photo"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="teacherstudent",
            name="comment",
        ),
        migrations.AddField(
            model_name="teacherstudent",
            name="level",
            field=models.CharField(blank=True, max_length=25),
        ),
        migrations.AlterField(
            model_name="teacherstudent",
            name="first_name",
            field=models.TextField(
                error_messages={"invalid": "Имя указанo некорректно"},
                validators=[
                    django.core.validators.RegexValidator(
                        message="Имя указано некорректно. Только латинские или только русские символы, первая буква заглавная, от 2 до 50 символов",
                        regex="^([А-ЯЁ]{1}[а-яё]{1,49})|([A-Z]{1}[a-z]{1,49})$",
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
                        message="Фамилия указана некорректно. Только латинские или только русские символы, первая буква заглавная, от 2 до 50 символов",
                        regex="^([А-ЯЁ]{1}[а-яё]{1,49})|([A-Z]{1}[a-z]{1,49})$",
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
                        message="Отчество указано некорректно. Только латинские или только русские символы, первая буква заглавная, от 2 до 50 символов",
                        regex="^([А-ЯЁ]{1}[а-яё]{1,49})|([A-Z]{1}[a-z]{1,49})$",
                    ),
                    django.core.validators.MinLengthValidator(2),
                    django.core.validators.MaxLengthValidator(50),
                ],
                verbose_name="Отчество",
            ),
        ),
        migrations.AlterField(
            model_name="teacherstudent",
            name="phone",
            field=models.TextField(
                null=True,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Телефон введен некорректно. От 11 до 13 символов. Введите в формате: 89051234567",
                        regex="^((\\+7|7|8)[0-9]{10,12})$",
                    ),
                    django.core.validators.MinLengthValidator(11),
                    django.core.validators.MaxLengthValidator(13),
                ],
                verbose_name="Телефон",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.TextField(
                error_messages={"invalid": "Имя указанo некорректно"},
                validators=[
                    django.core.validators.RegexValidator(
                        message="Имя указано некорректно. Только латинские или только русские символы, первая буква заглавная, от 2 до 50 символов",
                        regex="^([А-ЯЁ]{1}[а-яё]{1,49})|([A-Z]{1}[a-z]{1,49})$",
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
                        message="Фамилия указана некорректно. Только латинские или только русские символы, первая буква заглавная, от 2 до 50 символов",
                        regex="^([А-ЯЁ]{1}[а-яё]{1,49})|([A-Z]{1}[a-z]{1,49})$",
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
                        message="Отчество указано некорректно. Только латинские или только русские символы, первая буква заглавная, от 2 до 50 символов",
                        regex="^([А-ЯЁ]{1}[а-яё]{1,49})|([A-Z]{1}[a-z]{1,49})$",
                    ),
                    django.core.validators.MinLengthValidator(2),
                    django.core.validators.MaxLengthValidator(50),
                ],
                verbose_name="Отчество",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="phone",
            field=models.TextField(
                null=True,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Телефон введен некорректно. От 11 до 13 символов. Введите в формате: 89051234567",
                        regex="^((\\+7|7|8)[0-9]{10,12})$",
                    ),
                    django.core.validators.MinLengthValidator(11),
                    django.core.validators.MaxLengthValidator(13),
                ],
                verbose_name="Телефон",
            ),
        ),
    ]