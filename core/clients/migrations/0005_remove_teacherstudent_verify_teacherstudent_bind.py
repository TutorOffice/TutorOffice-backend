# Generated by Django 4.1.6 on 2023-04-04 15:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("clients", "0004_alter_teacherstudent_email_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="teacherstudent",
            name="verify",
        ),
        migrations.AddField(
            model_name="teacherstudent",
            name="bind",
            field=models.BooleanField(default=False, verbose_name="Привязка"),
        ),
    ]
