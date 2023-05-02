# Generated by Django 4.1.6 on 2023-05-02 19:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_alter_student_options_alter_teacher_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacherstudent',
            name='comment',
            field=models.TextField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='teacherstudent',
            name='first_name',
            field=models.TextField(error_messages={'invalid': 'Имя указанo некорректно'}, validators=[django.core.validators.RegexValidator(message='Имя указано некорректно.Только латинские или только русские символы, первая буква заглавная, от 2 до 50 символов', regex='^([А-ЯЁ]{1}[а-яё]{1,49})|([A-Z]{1}[a-z]{1,49})$'), django.core.validators.MinLengthValidator(2), django.core.validators.MaxLengthValidator(50)], verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='teacherstudent',
            name='last_name',
            field=models.TextField(error_messages={'invalid': 'Фамилия указана некорректно'}, validators=[django.core.validators.RegexValidator(message='Фамилия указана некорректно.Только латинские или только русские символы, первая буква заглавная, от 2 до 50 символов', regex='^([А-ЯЁ]{1}[а-яё]{1,49})|([A-Z]{1}[a-z]{1,49})$'), django.core.validators.MinLengthValidator(2), django.core.validators.MaxLengthValidator(50)], verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='teacherstudent',
            name='patronymic_name',
            field=models.TextField(blank=True, error_messages={'invalid': 'Отчество указанo некорректно'}, validators=[django.core.validators.RegexValidator(message='Отчество указано некорректно.Только латинские или только русские символы, первая буква заглавная, от 2 до 50 символов', regex='^([А-ЯЁ]{1}[а-яё]{1,49})|([A-Z]{1}[a-z]{1,49})$'), django.core.validators.MinLengthValidator(2), django.core.validators.MaxLengthValidator(50)], verbose_name='Отчество'),
        ),
        migrations.AlterField(
            model_name='teacherstudent',
            name='phone',
            field=models.TextField(null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Телефон введен некорректно.От 11 до 13 символов.Введите в формате: 89051234567', regex='^((\\+7|7|8)[0-9]{10,12})$'), django.core.validators.MinLengthValidator(11), django.core.validators.MaxLengthValidator(13)], verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.TextField(error_messages={'invalid': 'Имя указанo некорректно'}, validators=[django.core.validators.RegexValidator(message='Имя указано некорректно.Только латинские или только русские символы, первая буква заглавная, от 2 до 50 символов', regex='^([А-ЯЁ]{1}[а-яё]{1,49})|([A-Z]{1}[a-z]{1,49})$'), django.core.validators.MinLengthValidator(2), django.core.validators.MaxLengthValidator(50)], verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.TextField(error_messages={'invalid': 'Фамилия указана некорректно'}, validators=[django.core.validators.RegexValidator(message='Фамилия указана некорректно.Только латинские или только русские символы, первая буква заглавная, от 2 до 50 символов', regex='^([А-ЯЁ]{1}[а-яё]{1,49})|([A-Z]{1}[a-z]{1,49})$'), django.core.validators.MinLengthValidator(2), django.core.validators.MaxLengthValidator(50)], verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='user',
            name='patronymic_name',
            field=models.TextField(blank=True, error_messages={'invalid': 'Отчество указанo некорректно'}, validators=[django.core.validators.RegexValidator(message='Отчество указано некорректно.Только латинские или только русские символы, первая буква заглавная, от 2 до 50 символов', regex='^([А-ЯЁ]{1}[а-яё]{1,49})|([A-Z]{1}[a-z]{1,49})$'), django.core.validators.MinLengthValidator(2), django.core.validators.MaxLengthValidator(50)], verbose_name='Отчество'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.TextField(null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Телефон введен некорректно.От 11 до 13 символов.Введите в формате: 89051234567', regex='^((\\+7|7|8)[0-9]{10,12})$'), django.core.validators.MinLengthValidator(11), django.core.validators.MaxLengthValidator(13)], verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(null=True, upload_to='static/images/', verbose_name='Фотография'),
        ),
    ]
