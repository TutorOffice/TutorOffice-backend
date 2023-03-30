from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.shortcuts import get_object_or_404, redirect
from django.db.transaction import atomic
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

from .permissions import IsTeacher, IsTeacherOwner
from .serializers import *
from .models import User, Subject, Teacher, TeacherStudent
from .forms import CustomPasswordResetForm
from .services import Email
# Create your views here.


class RegisterViewSet(CreateModelMixin, GenericViewSet):
    """
    Регистрация пользователя и отправка
    сообщения для верификации почты
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    @atomic
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = get_object_or_404(User, pk=response.data['id'])
        token = RefreshToken.for_user(user)
        return Email.send_email(request, user, token)


class ActivateUserView(RetrieveAPIView):
    """
    Подтверждение верификации и
    перенаправление на профиль
    """

    def get(self, request, token, *args, **kwargs):
        try:
            # по refresh-токену проверяет валидность(срок) и идентифицирует пользователя
            user = User.objects.get(pk=RefreshToken(token).payload['user_id'])
        except (TokenError, User.DoesNotExist):
            user = None
        if user is None or user.is_active:
            return Response({"error": "Ссылка недействительна!"},
                            status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.save()
        # создание новых токенов для пользователя
        # token = RefreshToken.for_user(user)
        # создание ответа для перенаправления
        # добавление новых токенов в заголовки
        # response = redirect(reverse('login'))
        # response['Authorization'] = str(token.access_token)
        # response['refresh_token'] = str(token)
        return redirect(reverse('login'))


class TokenRegisterViewSet(CreateModelMixin, GenericViewSet):
    """Регистрация пользователя по приглашению"""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    @atomic
    def create(self, request, token, *args, **kwargs):
        # пытаюсь найти запись среди учеников учителей (TeacherStudent)
        try:
            obj = TeacherStudent.objects.get(pk=RefreshToken(token).payload['user_id'])
        except (TokenError, TeacherStudent.DoesNotExist):
            obj = None
        # Cрок годности истёк/ссылка подделана или
        # Если пользователь повторно использует ссылку
        if obj is None or obj.student is not None:
            return Response({"error": "Ссылка больше недействительна!"},
                            status=status.HTTP_400_BAD_REQUEST)
        # Если приглашённый пользователь указал аккаунт учителя
        if request.data['is_teacher']:
            return Response({"is_teacher": "Вы не можете зарегистрироваться как учитель!"})
        # создание и получение пользователя
        response = super().create(request, *args, **kwargs)
        user = get_object_or_404(User, pk=response.data['id'])
        # Если пользователь решил ввести другую почту, то она меняется и для преподавателя
        if user.email != obj.email:
            obj.email = user.email
            token = RefreshToken.for_user(user)
            return Email.send_email(request, user, token)
        # Если пользователь ввел ту же почту, то она сразу подтвержается
        user.is_active = True
        user.save()
        # добавляю внешний ключ на ученика в записи учителя (TeacherStudent)
        obj.student = user.student_profile
        obj.save()
        return redirect(reverse('login'))


class LoginView(TokenObtainPairView):
    """
    Вход, если почта не подтверждена,
    будет отправлено сообщение с подтверждением
    """

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(email=request.data['email'])
            if user.is_active:
                return super().post(request, *args, **kwargs)
                # нужен перевод исключений, если пароль не верен
            if user.check_password(request.data['password']):
                token = RefreshToken.for_user(user)
                return Email.send_email(request, user, token)
            raise User.DoesNotExist
        except User.DoesNotExist as error:
            return Response({"error": "Аккаунт с переданными учётными данными не найден!"},
                            status=status.HTTP_400_BAD_REQUEST)


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
        response = super().form_valid(form)
        send_mail(
            'Сброс пароля - успешно',
            'Ваш пароль был успешно сброшен!',
            # реализовать в service, добавить кнопку-ссылку на профиль, создать токен для пользователя
            # для редиректа на профиль
            settings.EMAIL_HOST_USER,
            [form.user.email],
            fail_silently=False,
        )
        return response


class SubjectsView(ListAPIView):
    """
    Получение всех предметов,
    только для аутентифицированных
    пользователей
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated, IsTeacher]
    # добавить пермишн для учителей


class UserSubjectViewSet(ModelViewSet):
    """
    Получение, обновление и
    добавление предметов репетитора
    """
    permission_classes = [IsAuthenticated, IsTeacher]
    # 5) добавить пермишн для учителей

    def get_queryset(self):
        return Subject.objects.filter(teachers__user=self.request.user)

    def get_object(self):
        return Teacher.objects.get(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return SubjectSerializer
        return UserSubjectSerializer


class ProfileViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class TeacherStudentsViewSet(CreateModelMixin, ListModelMixin,
                             UpdateModelMixin, DestroyModelMixin,
                             GenericViewSet):
    """Вьюха для CRUD-операций с учениками репетитора"""
    queryset = TeacherStudent
    serializer_class = TeacherStudentSerializer
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self):
        return TeacherStudent.objects.filter(teacher=self.request.user.teacher_profile)

    def get_permissions(self):
        if self.action in ('create', 'list'):
            return [IsAuthenticated(), IsTeacher()]
        return [IsAuthenticated(), IsTeacherOwner()]

    @atomic
    def perform_create(self, serializer):
        # сохраняю запись в бд, добавив внешний ключ
        teacher = self.request.user.teacher_profile
        obj = serializer.save(teacher=teacher)
        # проверяю наличие студента с указаной почтой в базе
        email = obj.email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if user:
            # если пользователь есть в базе отправляю ссылку на эндпоинт входа?
            pass
        else:
            # если пользователя нет в базе отправляю ссылку на эндпоинт регистрации
            jwt_token = RefreshToken.for_user(obj)
            Email.send_to_anonuser(self.request, email, jwt_token)
