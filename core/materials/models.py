from django.db import models
from clients.models import Teacher, TeacherStudent, Subject

# Create your models here.

PUBLIC = 'public'
PRIVATE = 'private'

TYPECHOICE = [
        (PUBLIC, 'public'),
        (PRIVATE, 'private'),
    ]


class Material(models.Model):
    """
    Модель для материалов как публичных, так и
    между преподавателем и студентом. При этом есть
    возможность рассылки.
    """

    teacher = models.ForeignKey(
        Teacher,
        related_name='materials',
        on_delete=models.PROTECT,
        verbose_name='Учитель')
    teacher_student = models.ManyToManyField(
        TeacherStudent,
        related_name='materials',
        verbose_name='Учитель-Ученик',)
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        verbose_name='Предмет')
    file = models.FileField(
        upload_to='static/materials/',
        blank=True,
        verbose_name='Файл материалов')
    text = models.TextField(
        verbose_name='Текст к материалу',
        blank=True)
    type = models.CharField(
        max_length=10,
        choices=TYPECHOICE,
        default=PRIVATE,
        verbose_name='Тип материалов')

    def __str__(self):
        return f'{self.subject}'

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'
        ordering = ('subject', 'teacher')
