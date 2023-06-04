# Generated by Django 4.2.1 on 2023-06-02 20:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("clients", "0010_alter_user_photo"),
        ("lessons", "0004_alter_lesson_status"),
    ]

    operations = [
        migrations.RenameField(
            model_name="lesson",
            old_name="comment",
            new_name="student_comment",
        ),
        migrations.RemoveField(
            model_name="lesson",
            name="topic",
        ),
        migrations.AddField(
            model_name="lesson",
            name="teacher_comment",
            field=models.TextField(blank=True, verbose_name="Комментарий"),
        ),
        migrations.AlterField(
            model_name="lesson",
            name="subject",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="clients.subject",
                verbose_name="Предмет",
            ),
        ),
    ]