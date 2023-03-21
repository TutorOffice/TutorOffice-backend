from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.shortcuts import get_object_or_404, redirect, Http404
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

from .permissions import IsTeacher
from .serializers import RegisterSerializer, SubjectSerializer, UserSubjectSerializer, ProfileSerializer
from .models import User, Subject, Teacher
from .forms import CustomPasswordResetForm
from .services import Email
# Create your views here.


class RegisterView(CreateModelMixin, GenericViewSet):
    """
    Регистрация пользователя и отправка
    сообщения для верификации почты
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

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
        if User is None or user.is_active:
            return Response({"ERROR": "Ссылка недействительна!"},
                            status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.save()
        # создание новых токенов для пользователя
        token = RefreshToken.for_user(user)
        # создание ответа для перенаправления и добавление токенов в заголовки
        response = redirect(reverse('profile'))
        response['access_token'] = str(token.access_token)
        response['refresh_token'] = str(token)
        return response


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
            return Response({"ERROR": "Аккаунт с переданными учётными данными не найден!"},
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


class ProfileViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class SubjectsView(ListAPIView):
    """
    Получение всех предметов,
    только для аутентифицированных
    пользователей
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated, IsTeacher]
    authentication_classes = [JWTAuthentication]
    # добавить пермишн для учителей


class UserSubjectViewSet(ModelViewSet):
    """
    Получение, обновление и
    добавление предметов репетитора
    """
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated, IsTeacher]
    authentication_classes = [JWTAuthentication]
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
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        return self.request.user
