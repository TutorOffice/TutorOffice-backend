# Generated by Django 4.1.6 on 2023-04-07 20:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("clients", "0005_remove_teacherstudent_verify_teacherstudent_bind"),
    ]

    operations = [
        migrations.AlterField(
            model_name="teacherstudent",
            name="bind",
            field=models.CharField(
                choices=[
                    ("unrelated", "unrelated"),
                    ("awaiting", "awaiting"),
                    ("related", "related"),
                ],
                default="unrelated",
                max_length=10,
                verbose_name="Привязка",
            ),
        ),
    ]
