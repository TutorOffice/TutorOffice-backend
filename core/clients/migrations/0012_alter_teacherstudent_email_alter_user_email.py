# Generated by Django 4.2.1 on 2023-06-06 13:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "clients",
            "0011_remove_teacherstudent_comment_teacherstudent_level_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="teacherstudent",
            name="email",
            field=models.EmailField(
                error_messages={"invalid": "E-mail введен некорректно!"},
                max_length=50,
                validators=[
                    django.core.validators.EmailValidator(),
                    django.core.validators.MinLengthValidator(7),
                    django.core.validators.MaxLengthValidator(254),
                ],
                verbose_name="Электронная почта",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                error_messages={"invalid": "E-mail введен некорректно!"},
                max_length=50,
                unique=True,
                validators=[
                    django.core.validators.EmailValidator(),
                    django.core.validators.MinLengthValidator(7),
                    django.core.validators.MaxLengthValidator(254),
                ],
                verbose_name="Электронная почта",
            ),
        ),
    ]
