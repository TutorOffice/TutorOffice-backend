# Generated by Django 4.1.6 on 2023-04-09 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_alter_student_options_alter_teacher_options_and_more'),
        ('lessons', '0004_alter_lesson_homework'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='homework',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='lessons.homework', verbose_name='Домашняя работа'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='teacher_student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='lessons', to='clients.teacherstudent', verbose_name='Учитель-Ученик'),
        ),
    ]