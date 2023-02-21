from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Создаёт и сохраняет пользователя с заданной почтой и паролем
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class Subject(models.Model):
    """
    Модель для категорий предметов,
    по которым будут распределяться учителя
    """
    title = models.TextField(max_length=30,
                             unique=True,
                             db_index=True)

    def __str__(self):
        return {self.title}

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        ordering = ('title',)


class User(AbstractUser):
    """Модель для описания юзера (ученика)"""

    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
    )
    first_name = models.TextField(
        "Имя",
        max_length=20,
    )
    last_name = models.TextField(
        "Фамилия",
        max_length=20,
    )
    email = models.EmailField(
        "Электронная почта",
        max_length=254,
        unique=True,
    )
    phone = models.TextField(
        "Телефон",
        max_length=14,
        unique=True,
    )
    email_verify = models.BooleanField(
        "Подтвержден e-mail",
        default=False,
    )
    photo = models.ImageField(
        "Фотография",
        upload_to='images/',
        blank=True,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('last_name', 'first_name')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager


class Student(models.Model):
    """Модель, расширяющая юзера, позволяя быть студентом"""
    profile = models.OneToOneField(User,
                                   related_name='student_profile',
                                   on_delete=models.PROTECT)


class Teacher(models.Model):
    """Модель, расширяющая юзера, позволяя быть репетитором"""
    profile = models.OneToOneField(User,
                                   related_name='teacher_profile',
                                   on_delete=models.PROTECT)
    students = models.ManyToManyField(Student,
                                      related_name='teachers',
                                      through="TeacherStudent")
    subjects = models.ManyToManyField(Subject,
                                      related_name='teachers',
                                      blank=True
                                      )

    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'


class TeacherStudent(models.Model):
    """
    Модель, связывающая преподавателя со студентом.
    Также предоставляет возможность создания учителю 'собственных' учеников
    """
    teacher = models.ForeignKey(
        Teacher,
        related_name='studentM2M',
        on_delete=models.PROTECT,
    )
    student = models.ForeignKey(
        Student,
        related_name='teacherM2M',
        on_delete=models.PROTECT,
    )
    first_name = models.TextField(
        "Имя ученика",
        max_length=20,
    )
    last_name = models.TextField(
        "Фамилия ученика",
        max_length=20,
    )
    email = models.EmailField(
        "Электронная почта",
        max_length=254,
        unique=True,
    )
    verify = models.BooleanField(
        "Подтверждение",
        default=False,
    )
    comment = models.TextField()

