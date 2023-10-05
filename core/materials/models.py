from clients.models import Subject, Teacher, TeacherStudent
from django.db import models

# Create your models here.

PUBLIC = "public"
PRIVATE = "private"

TYPECHOICE = [
    (PUBLIC, "public"),
    (PRIVATE, "private"),
]


class Material(models.Model):
    """
    Модель для материалов как публичных, так и
    между преподавателем и студентом. При этом есть
    возможность рассылки.
    """

    teacher = models.ForeignKey(
        Teacher,
        related_name="materials",
        on_delete=models.CASCADE,
        verbose_name="Учитель",
    )
    teacher_student = models.ManyToManyField(
        TeacherStudent,
        related_name="materials",
        verbose_name="Учитель-Ученик",
        blank=True,
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        verbose_name="Предмет",
        null=True
    )
    file = models.FileField(
        upload_to="materials/",
        verbose_name="Файл материалов"
    )
    file_type = models.CharField(
        max_length=25,
        verbose_name="Тип файла",
        null=True,
    )
    file_size = models.IntegerField(
        verbose_name="Размер файла (КБ)",
        null=True,
    )
    text = models.TextField(
        verbose_name="Текст к материалу",
        blank=True,
    )
    material_type = models.CharField(
        max_length=10,
        choices=TYPECHOICE,
        default=PRIVATE,
        verbose_name="Тип материалов",
    )
    date = models.DateField(
        verbose_name="дата",
        auto_now=True,
    )

    def __str__(self):
        return f"{self.subject}"

    class Meta:
        verbose_name = "Материал"
        verbose_name_plural = "Материалы"
        ordering = ("subject", "teacher")
