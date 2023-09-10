import uuid

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    UserManager,
)
from django.core.validators import (
    EmailValidator,
    MaxLengthValidator,
    MinLengthValidator,
    RegexValidator,
)
from django.db import models

#  length of first_name, last_name, patronymic_name from 2 to 50
REGEX_NAME_VALIDATOR = "^([А-ЯЁ]{1}[а-яё]{1,49})|([A-Z]{1}[a-z]{1,49})$"
NAME_MIN_LENGTH = 2
NAME_MAX_LENGTH = 50
EMAIL_MIN_LENGTH = 7
EMAIL_MAX_LENGTH = 254
PHONE_MIN_LENGTH = 11
PHONE_MAX_LENGTH = 13

UNRELATED = "unrelated"
AWAITING = "awaiting"
RELATED = "related"

TYPECHOICE = [
    (UNRELATED, "unrelated"),
    (AWAITING, "awaiting"),
    (RELATED, "related"),
]


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Создаёт и сохраняет пользователя с заданной почтой и паролем
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
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
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")

        return self._create_user(email, password, **extra_fields)


class Subject(models.Model):
    """
    Предметы, связаны только с учителями через М2М
    """

    title = models.TextField(max_length=30, unique=True, db_index=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"
        ordering = ("title",)


class User(AbstractBaseUser, PermissionsMixin):
    """Пользователи"""

    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
    )
    first_name = models.TextField(
        "Имя",
        validators=[
            RegexValidator(
                regex=REGEX_NAME_VALIDATOR,
                message="Имя указано некорректно. "
                "Только латинские или "
                "только русские символы, "
                "первая буква заглавная, "
                "от 2 до 50 символов",
            ),
            MinLengthValidator(NAME_MIN_LENGTH),
            MaxLengthValidator(NAME_MAX_LENGTH),
        ],
        error_messages={"invalid": "Имя указанo некорректно"},
    )
    patronymic_name = models.TextField(
        "Отчество",
        blank=True,
        validators=[
            RegexValidator(
                regex=REGEX_NAME_VALIDATOR,
                message="Отчество указано некорректно. "
                "Только латинские или "
                "только русские символы, "
                "первая буква заглавная, "
                "от 2 до 50 символов",
            ),
            MinLengthValidator(NAME_MIN_LENGTH),
            MaxLengthValidator(NAME_MAX_LENGTH),
        ],
        error_messages={"invalid": "Отчество указанo некорректно"},
    )
    last_name = models.TextField(
        "Фамилия",
        validators=[
            RegexValidator(
                regex=REGEX_NAME_VALIDATOR,
                message="Фамилия указана некорректно. "
                "Только латинские или "
                "только русские символы, "
                "первая буква заглавная, "
                "от 2 до 50 символов",
            ),
            MinLengthValidator(NAME_MIN_LENGTH),
            MaxLengthValidator(NAME_MAX_LENGTH),
        ],
        error_messages={"invalid": "Фамилия указана некорректно"},
    )
    phone = models.TextField(
        "Телефон",
        unique=True,
        null=True,
        validators=[
            RegexValidator(
                regex="^((\+7|7|8)[0-9]{10,12})$",
                message="Телефон введен некорректно. "
                        "От 11 до 13 символов. Введите в формате: 89051234567",
            ),
            MinLengthValidator(PHONE_MIN_LENGTH),
            MaxLengthValidator(PHONE_MAX_LENGTH),
        ],
    )
    email = models.EmailField(
        "Электронная почта",
        max_length=50,
        unique=True,
        validators=[
            EmailValidator(),
            MinLengthValidator(EMAIL_MIN_LENGTH),
            MaxLengthValidator(EMAIL_MAX_LENGTH),
        ],
        error_messages={"invalid": "E-mail введен некорректно!"},
    )
    is_active = models.BooleanField(
        "Подтверждение",
        default=False,
    )
    photo = models.ImageField(
        "Фотография",
        upload_to="profiles/",
        null=True,
    )
    is_staff = models.BooleanField(
        "Доступ к админке",
        default=False,
    )

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("last_name", "first_name")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class Student(models.Model):
    """Модель, расширяющая юзера, позволяя быть студентом"""

    user = models.OneToOneField(
        User,
        related_name="student_profile",
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
        ordering = ("user",)

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"


class Teacher(models.Model):
    """Модель, расширяющая юзера, позволяя быть репетитором"""

    user = models.OneToOneField(
        User,
        related_name="teacher_profile",
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    students = models.ManyToManyField(
        Student,
        related_name="teachers",
        through="TeacherStudent",
        verbose_name="Студенты",
    )
    subjects = models.ManyToManyField(
        Subject,
        related_name="teachers",
        blank=True,
        verbose_name="Предметы",
    )

    class Meta:
        verbose_name = "Учитель"
        verbose_name_plural = "Учителя"
        ordering = ("user",)

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"


class TeacherStudent(models.Model):
    """
    Модель, связывающая репетитора со студентом.
    Также предоставляет возможность создания учителю собственных
    непривязанных учеников
    """

    teacher = models.ForeignKey(
        Teacher,
        related_name="studentM2M",
        on_delete=models.CASCADE,
        verbose_name="Учитель",
    )
    student = models.ForeignKey(
        Student,
        related_name="teacherM2M",
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Студент",
    )
    first_name = models.TextField(
        "Имя",
        validators=[
            RegexValidator(
                regex=REGEX_NAME_VALIDATOR,
                message="Имя указано некорректно. "
                "Только латинские или "
                "только русские символы, "
                "первая буква заглавная, "
                "от 2 до 50 символов",
            ),
            MinLengthValidator(NAME_MIN_LENGTH),
            MaxLengthValidator(NAME_MAX_LENGTH),
        ],
        error_messages={"invalid": "Имя указанo некорректно"},
    )
    patronymic_name = models.TextField(
        "Отчество",
        blank=True,
        validators=[
            RegexValidator(
                regex=REGEX_NAME_VALIDATOR,
                message="Отчество указано некорректно. "
                "Только латинские или "
                "только русские символы, "
                "первая буква заглавная, "
                "от 2 до 50 символов",
            ),
            MinLengthValidator(NAME_MIN_LENGTH),
            MaxLengthValidator(NAME_MAX_LENGTH),
        ],
        error_messages={"invalid": "Отчество указанo некорректно"},
    )
    last_name = models.TextField(
        "Фамилия",
        validators=[
            RegexValidator(
                regex=REGEX_NAME_VALIDATOR,
                message="Фамилия указана некорректно. "
                "Только латинские или "
                "только русские символы, "
                "первая буква заглавная, "
                "от 2 до 50 символов",
            ),
            MinLengthValidator(NAME_MIN_LENGTH),
            MaxLengthValidator(NAME_MAX_LENGTH),
        ],
        error_messages={"invalid": "Фамилия указана некорректно"},
    )
    phone = models.TextField(
        "Телефон",
        unique=True,
        null=True,
        validators=[
            RegexValidator(
                regex="^((\+7|7|8)[0-9]{10,12})$",
                message="Телефон введен некорректно. "
                        "От 11 до 13 символов. Введите в формате: 89051234567",
            ),
            MinLengthValidator(PHONE_MIN_LENGTH),
            MaxLengthValidator(PHONE_MAX_LENGTH),
        ],
    )
    email = models.EmailField(
        "Электронная почта",
        max_length=50,
        validators=[
            EmailValidator(),
            MinLengthValidator(EMAIL_MIN_LENGTH),
            MaxLengthValidator(EMAIL_MAX_LENGTH),
        ],
        error_messages={"invalid": "E-mail введен некорректно!"},
    )
    bind = models.CharField(
        "Привязка",
        max_length=10,
        choices=TYPECHOICE,
        default=UNRELATED,
    )
    level = models.CharField(blank=True, max_length=25)

    class Meta:
        verbose_name = "Псевдоученик"
        verbose_name_plural = "Псевдоученики"
        ordering = ("teacher",)

    def __str__(self):
        return f"{self.teacher} {self.last_name} {self.first_name}"
