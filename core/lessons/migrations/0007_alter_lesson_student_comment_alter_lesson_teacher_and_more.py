# Generated by Django 4.2.1 on 2023-06-09 10:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("clients", "0013_alter_teacherstudent_options"),
        (
            "lessons",
            "0006_alter_lesson_student_comment_alter_lesson_subject_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="lesson",
            name="student_comment",
            field=models.TextField(
                blank=True, max_length=100, verbose_name="Комментарий ученика"
            ),
        ),
        migrations.AlterField(
            model_name="lesson",
            name="teacher",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="t_lessons",
                to="clients.teacher",
                verbose_name="Учитель",
            ),
        ),
        migrations.AlterField(
            model_name="lesson",
            name="teacher_comment",
            field=models.TextField(
                blank=True,
                max_length=100,
                verbose_name="Комментарий репетитора",
            ),
        ),
        migrations.AlterField(
            model_name="lesson",
            name="teacher_student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="ts_lessons",
                to="clients.teacherstudent",
                verbose_name="Псевдоученик",
            ),
        ),
        migrations.DeleteModel(
            name="Homework",
        ),
    ]
