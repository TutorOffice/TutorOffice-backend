# Generated by Django 4.2.1 on 2023-09-10 20:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("clients", "0014_alter_student_user_alter_teacher_user_and_more"),
        ("materials", "0010_rename_type_material_material_type_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="material",
            name="subject",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="clients.subject",
                verbose_name="Предмет",
            ),
        ),
        migrations.AlterField(
            model_name="material",
            name="teacher",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="materials",
                to="clients.teacher",
                verbose_name="Учитель",
            ),
        ),
    ]
