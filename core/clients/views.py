import logging

from django.conf import settings
from django.contrib.auth.views import (
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.contrib.sites.shortcuts import get_current_site
from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import (
    GenericViewSet,
    ModelViewSet,
    ReadOnlyModelViewSet,
)
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .forms import CustomPasswordResetForm
from .models import Student, Subject, Teacher, TeacherStudent, User
from .pagination import SubjectsPagination, UsersPagination
from .permissions import IsStudent, IsTeacher, IsTeacherOwner
from .serializers import (
    ProfileSerializer,
    RegisterSerializer,
    StudentTeacherSerializer,
    StudentTeacherDetailSerializer,
    SubjectSerializer,
    TeacherStudentDetailSerializer,
    TeacherStudentSerializer,
    UserSubjectSerializer,
)
from .services import get_user_type
from .tasks import Email

logger = logging.getLogger(__name__)


class RegisterViewSet(CreateModelMixin, GenericViewSet):
    """
    Регистрация пользователя и отправка
    сообщения для верификации почты
    """

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    http_method_names = ("post",)

    @atomic
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = get_object_or_404(User, pk=response.data["id"])
        logger.info(f"Пользователь с почтой {user.email} зарегистрирован!")
        token = RefreshToken.for_user(user)
        template = "clients/activate.html"
        email_subject = (
            "Подтвердите почту для активации вашего кабинета репетитора"
        )
        to_email = user.email
        context = {
            "token": str(token),
            "full_name": f"{user.last_name} {user.first_name}",
        }
        domain = str(get_current_site(request))
        logger.info(
            f"Отправка подтверждения почты в celery для юзера {to_email}"
        )
        Email.send_email_task.delay(
            domain, template, email_subject, context, to_email
        )
        logger.info(
            f"Подтверждение почты для юзера {to_email} отправлено в celery"
        )
        return Response(
            {
                "success": "Регистрация прошла успешно! "
                           "Вам было отправлено письмо "
                           "с подтверждением на почту!"
            },
            status=status.HTTP_201_CREATED,
        )


class ActivateUserView(APIView):
    """Верификация почты"""

    def post(self, request, token, *args, **kwargs):
        try:
            # по refresh-токену проверяет валидность(срок)
            # и идентифицируется пользователь
            user = User.objects.get(pk=RefreshToken(token).payload["user_id"])
        except (TokenError, User.DoesNotExist):
            user = None
        if user is None or user.is_active:
            logger.info(f"Юзер не прошёл верификацию почты")
            return Response(
                {"detail": "Ссылка недействительна"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.is_active = True
        user.save()
        logger.info(f"Юзер {user.email} прошёл верификацию почты!")
        refresh = RefreshToken.for_user(user)
        # добавляется тип пользователя, нужно для фронта
        request.user = user
        role = get_user_type(request)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "role": role,
            },
            status=status.HTTP_200_OK,
        )


class LoginView(TokenObtainPairView):
    """
    Вход, если почта не подтверждена,
    будет отправлено сообщение с подтверждением
    """

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        if email and password:
            try:
                user = User.objects.get(email=request.data["email"])
                if user.is_active:
                    response = super().post(request, *args, **kwargs)
                    # добавляется тип пользователя, нужно для фронта
                    request.user = user
                    role = get_user_type(request)
                    response.data["role"] = role
                    logger.info(f"{user.email} вошёл в систему")
                    return response
                if user.check_password(password):
                    logger.info(
                        f"Неактивный пользователь {user.email} "
                        f"совершил попытку входа"
                    )
                    token = RefreshToken.for_user(user)
                    template = "clients/activate.html"
                    email_subject = "Подтвердите почту для активации вашего кабинета репетитора"
                    to_email = user.email
                    context = {
                        "token": str(token),
                        "full_name": f"{user.last_name} {user.first_name}",
                    }
                    domain = str(get_current_site(request))
                    logger.info(
                        f"Отправка подтверждения почты в celery для юзера {to_email}"
                    )
                    Email.send_email_task.delay(
                        domain, template, email_subject, context, to_email
                    )
                    logger.info(
                        f"Подтверждение почты для юзера {to_email} отправлено в celery"
                    )
                    return Response(
                        {
                            "detail": "Ваша почта не подтверждена! "
                            "На неё было отправлено новое письмо с подтверждением!"
                        },
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
                raise User.DoesNotExist
            except User.DoesNotExist:
                logger.warning(f"Пользователь с почтой {email} не найден!")
                return Response(
                    {
                        "detail": "Не найдено активной учетной записи с указанными данными"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response({"detail": "Все поля должны быть заполнены!"})


class CustomPasswordResetView(PasswordResetView):
    """
    Стандартный класс django для обработки почты и
    отправки сообщения о сбросе пароля
    """

    # Рабочая почта используется в качестве отправителя
    from_email = settings.EMAIL_HOST_USER
    form_class = CustomPasswordResetForm


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Стандартный класс django для обработки
    новых паролей пользователя
    """

    # template_name = 'reset.html' добавить кнопку-ссылку по ТЗ

    def form_valid(self, form):
        # Отправляется сообщение об успешном сбросе пароля на почту пользователя
        logger.info(f"Пользователь {form.user.email} успешно сбросил пароль!")
        response = super().form_valid(form)
        logger.info(
            f"Отправка уведомления об успешном сбросе пароля "
            f"в celery для юзера {form.user.email}"
        )
        Email.send_email_task.delay(
            email_subject="Сброс пароля - успешно",
            message="Ваш пароль был успешно сброшен!",
            from_email=settings.EMAIL_HOST_USER,
            to_email=form.user.email,
        )
        logger.info(
            f"Сообщение об успешном сбросе пароля"
            f" для юзера {form.user.email} отправлено в celery"
        )
        return response


@method_decorator(cache_page(60 * 15), name="dispatch")
class SubjectsView(ListAPIView):
    """
    Получение всех предметов,
    только для аутентифицированных
    пользователей
    """

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = (IsAuthenticated, IsTeacher)
    pagination_class = SubjectsPagination
    # добавить пермишн для учителей


@method_decorator(cache_page(60 * 15), name="dispatch")
class UserSubjectViewSet(ModelViewSet):
    """
    Получение, обновление и
    добавление предметов репетитора
    """

    permission_classes = [IsAuthenticated, IsTeacher]
    pagination_class = SubjectsPagination
    http_method_names = (
        "get",
        "patch",
        "post",
    )
    # 5) добавить пермишн для учителей

    def get_queryset(self):
        """Получение всех предметов преподавателя"""
        user = self.request.user
        return Subject.objects.filter(teachers__user=user)

    def get_object(self):
        """
        Получение профиля преподавателя
        для обновления перечня его предметов
        """
        user = self.request.user
        return Teacher.objects.get(user=user)

    def get_serializer_class(self):
        if self.action == "list":
            return SubjectSerializer
        return UserSubjectSerializer


@method_decorator(cache_page(60 * 5), name="dispatch")
class ProfileViewSet(
    RetrieveModelMixin, UpdateModelMixin, GenericViewSet
):
    """Получение и обновление профиля пользователя"""

    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ("get", "patch")

    def get_object(self):
        return self.request.user


@method_decorator(cache_page(60 * 5), name="dispatch")
class TeacherStudentViewSet(ModelViewSet):
    pagination_class = UsersPagination
    http_method_names = ['post', 'patch', 'delete', 'get']

    def get_permissions(self):
        """
        Эндпоинт доступен только для репетиторов.
        Изменять, удалять и получать записи отдельных
        псевдоучеников может только репетитор,
        который их создал.
        """
        if self.action in ("partial_update", "destroy", "retrieve"):
            return [IsAuthenticated(), IsTeacherOwner()]
        return [IsAuthenticated(), IsTeacher()]

    def get_serializer_class(self):
        if self.action in ("partial_update", "destroy", "retrieve"):
            return TeacherStudentDetailSerializer
        return TeacherStudentSerializer

    def get_object(self):
        """Получение псевдоученика репетитора"""
        pk = self.kwargs['pk']
        user = self.request.user
        return get_object_or_404(
            TeacherStudent.objects.select_related(
                "student__user", "teacher__user"
            ).all(),
            pk=pk,
            teacher=user.teacher_profile
        )

    def get_queryset(self):
        """
        Получение записей псевдоучеников для
        текущего пользователя-репетитора
        """
        teacher = self.request.user.teacher_profile
        return TeacherStudent.objects.select_related("student__user").filter(
            teacher=teacher
        )

    def perform_create(self, serializer):
        """
        Сохраняет запись в бд, добавив
        внешний ключ на учителя
        """

        teacher = self.request.user.teacher_profile
        serializer.save(teacher=teacher)

    def destroy(self, request, *args, **kwargs):
        """
        Удаление ученика вместе с назначенными для него уроками
        """

        obj = self.get_object()
        logger.info(
            "Удаление ученика и уроков" f" юзера - {request.user.email}"
        )
        obj.lessons.all().delete()
        return super().destroy(request, *args, **kwargs)


class RelateUnrelateStudentView(APIView):
    """
    Вьюха для отправки запросов
    на добавление (привзяку к псевдоученику)
    и отвязки ученика учителем от псевдоученика
    """

    permission_classes = [IsAuthenticated, IsTeacher]

    def post(self, request, pk, format=None):
        """
        Отправляет запрос на добавление ученику, если он есть в базе
        запрашивает подтверждения, если ученика нет в базе,
        то просто предлагает зарегистрироваться
        """
        # получение записи из таблицы TeacherStudent по её id
        try:
            logger.info(
                f"Репетитор {request.user.email} пытается "
                f"отправить запрос на привязку ученика"
            )
            obj = TeacherStudent.objects.get(pk=pk)
        except TeacherStudent.DoesNotExist:
            return Response({"detail": "Такой записи не существует!"})
        if obj.teacher.user != request.user:
            return Response(
                {"detail": "У вас нет прав на осуществление этого действия!"}
            )
        if obj.student:
            return Response({"detail": "К данной записи ученик уже привязан!"})
        email = obj.email
        # проверка наличия пользователя с такой почтой в базе
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        to_email = obj.email
        template = "clients/relation.html"
        context = {
            "teacher_name": f"{request.user.first_name} {request.user.last_name}",
        }
        domain = str(get_current_site(request))
        # если пользователь есть в базе, отправляется ссылка на подтверждение
        if user:
            try:
                student_profile = user.student_profile
            except Student.DoesNotExist:
                return Response(
                    {
                        "detail": "Вы не можете добавить этого пользователя, "
                                  "так как он не является учеником!"
                    }
                )
            email_subject = "Подтвердите запрос от репетитора!"
            context["student_name"] = f"{user.last_name} {user.first_name}"
            context["url_name"] = "confirm"
            # !Нужно будет изменить имя на то, что будет определено в сеттингс
            # токен будет использоваться в ссылке, для связи записей ученика и TeacherStudent
            token = RefreshToken.for_user(obj)
            token["student"] = student_profile.id
            context["token"] = str(token)
        # если пользователя нет в базе, отправляется запрос на регистрацию
        else:
            email_subject = (
                "Зарегистрируйтесь и подтвердите запрос от репетитора!"
            )
            context["url_name"] = "register-list"
            # !Нужно будет изменить имя на то, что будет определено в сеттингс
        logger.info(
            f"Отправка запроса на привязку ученика - {to_email}"
            f" для репетитора {request.user.email} в celery"
        )
        Email.send_email_task.delay(
            domain, template, email_subject, context, to_email
        )
        logger.info(
            f"Запрос на привзяку ученика - {to_email}"
            f" для репетитора {request.user.email} отправлен в celery"
        )
        obj.bind = "awaiting"
        obj.save()
        return Response(
            {
                "success": "Ваш запрос был успешно "
                           "отправлен на почту пользователю!"
            },
            status=status.HTTP_200_OK,
        )

    def patch(self, request, pk, format=None):
        """
        Метод для отвязки ученика от
        псевдоученика учителя
        """
        try:
            logger.info(
                f"Репетитор {request.user.email} пытается отвязать ученика"
            )
            obj = TeacherStudent.objects.get(pk=pk)
        except TeacherStudent.DoesNotExist:
            return Response({"detail": "Такой записи не существует!"})
        if obj.teacher.user != request.user:
            return Response(
                {"detail": "У вас нет прав на осуществление этого действия!"}
            )
        if not obj.student:
            return Response({"detail": "К этой записи не привязан ученик!"})
        obj.student = None
        obj.bind = "unrelated"
        obj.save()
        logger.info(
            f"Репетитор {request.user.email} отвязал ученика "
            f"от псевдоученика {obj.email}"
        )
        return Response({"success": "Ученик был успешно отвязан от вас!"})


class ConfirmView(APIView):
    """
    Подтверждение учеником привязки к репетитору
    """

    def post(self, request, token):
        try:
            obj = TeacherStudent.objects.get(
                pk=RefreshToken(token).payload["user_id"]
            )
        except (TokenError, TeacherStudent.DoesNotExist):
            obj = None
        if obj is None or obj.student:
            return Response(
                {"detail": "Ссылка больше недействительна!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        student_id = RefreshToken(token).payload["student"]
        student = Student.objects.get(pk=student_id)
        obj.student = student
        obj.bind = "related"
        obj.save()
        logger.info(
            f"Ученик {obj.email} привязался к псевдоученику "
            f"репетитора {obj.teacher.user.email}"
        )
        # Отправка уведомления учителю о добавлении
        logger.info(
            f"Отправка сообщения об успешной привязке в celery "
            f"для репетитора {obj.teacher.user.email}"
        )
        Email.send_email_task.delay(
            email_subject="Ученик подтвердил запрос на добавление!",
            message=(
                f"Пользователь {obj.last_name} {obj.first_name} подтвердил"
                f"запрос на его добавление в качестве ученика!"
            ),
            from_email=settings.EMAIL_HOST_USER,
            to_email=obj.teacher.user.email,
        )
        logger.info(
            f"Cообщение об успешной привязке отправлено в celery для репетитора {obj.teacher.user.email}"
        )
        return Response(
            {"success": "Вы были успешно добавлены к репетитору!"},
            status=status.HTTP_200_OK,
        )


@method_decorator(cache_page(60 * 5), name="dispatch")
class StudentTeachersViewSet(ReadOnlyModelViewSet):
    """
    Просмотр списка репетиторов ученика
    и отдельно взятого репетитора ученика
    """

    pagination_class = UsersPagination
    serializer_class = StudentTeacherSerializer

    def get_permissions(self):
        """Эндпоинт доступен только для учеников"""
        if self.action == "list":
            return [IsAuthenticated(), IsStudent()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == "list":
            return StudentTeacherSerializer
        return StudentTeacherDetailSerializer

    def get_queryset(self):
        """
        Получение списка репетиторов
        текущего пользователя-ученика
        """
        user = self.request.user
        return User.objects.select_related(
            'teacher_profile',
        ).filter(
            teacher_profile__studentM2M__student=user.student_profile
        )

    def get_object(self):
        """
        Получение конкретного репетитора,
        текущего пользователя-ученика
        """
        pk = self.kwargs['pk']
        user = self.request.user
        return get_object_or_404(
            User.objects.select_related(
                'teacher_profile'
            ).prefetch_related(
                'teacher_profile__subjects'
            ).all(),
            pk=pk,
            teacher_profile__studentM2M__student=user.student_profile
        )
