from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.serializers import  TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.shortcuts import get_object_or_404, redirect
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

from .permissions import IsTeacher, IsTeacherOwner
from .serializers import *
from .models import User, Subject, Teacher, TeacherStudent
from .forms import CustomPasswordResetForm
from .services import Email

from smtplib import SMTPDataError
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
        try:
            email_subject = 'Подтвердите почту для активации вашего кабинета репетитора'
            template = 'clients/activate.html'
            to_email = [user.email]
            context = {
                "token": token,
                "full_name": f"{user.last_name} {user.first_name}"
             }
            return Email.send_email(request, email_subject, template, context, to_email)
        except SMTPDataError:
            # отмена сохранения записи в бд
            transaction.set_rollback(True)
            return Response({"error": "Почта не найдена! "
                             "Невозможно отправить сообщение для подтверждения!"},
                            status=status.HTTP_400_BAD_REQUEST)


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
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


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
            if user.check_password(request.data['password']):
                token = RefreshToken.for_user(user)
                try:
                    email_subject = 'Подтвердите почту для активации вашего кабинета репетитора'
                    template = 'clients/activate.html'
                    to_email = [user.email]
                    context = {
                        "token": token,
                        "full_name": f"{user.last_name} {user.first_name}"
                    }
                    return Email.send_email(request, email_subject, template, context, to_email)
                except SMTPDataError:
                    return Response({"error": "Почта не найдена! "
                                              "Невозможно отправить сообщение для подтверждения!"},
                                    status=status.HTTP_400_BAD_REQUEST)
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
            subject='Сброс пароля - успешно',
            message='Ваш пароль был успешно сброшен!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[form.user.email],
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

    # def get_permissions(self):
    #     if self.action in ('create', 'list'):
    #         return [IsAuthenticated(), IsTeacher()]
    #     return [IsAuthenticated(), IsTeacherOwner()]

    def perform_create(self, serializer):
        # сохраняется запись в бд, добавив учителя
        teacher = self.request.user.teacher_profile
        serializer.save(teacher=teacher)

    # def send_add_request(self, request, response):
    #     obj = TeacherStudent.objects.get(pk=response.data['id'])
    #     email = obj.email
    #     # проверяется наличие студента с указанной почтой в базе
    #     try:
    #         user = User.objects.get(email=email)
    #     except User.DoesNotExist:
    #         user = None
    #     token = RefreshToken.for_user(obj)
    #     to_email = [obj.email]
    #     template = 'clients/addition.html'
    #     context = {
    #         "token": token,
    #         "teacher_name": f"{request.user.first_name} {request.user.last_name}",
    #     }
    #     # если пользователь есть в базе отправляю ссылку на эндпоинт входа
    #     if user:
    #         email_subject = 'Подтвердите запрос от репетитора!'
    #         context['student_name'] = f"{user.last_name} {user.first_name}"
    #         context['url_name'] = 'confirm'
    #     # если пользователя нет в базе отправляю ссылку на почту для эндпоинта регистрации
    #     else:
    #         email_subject = 'Зарегистрируйтесь и подтвердите запрос от репетитора!'
    #         context['url_name'] = 'register'
    #     return Email.send_email(self.request, email_subject, template, context, to_email)


# class ConfirmAddView(APIView):
#     def get(self, request, token):
#         try:
#             obj = TeacherStudent.objects.get(pk=RefreshToken(token).payload['user_id'])
#         except (TokenError, TeacherStudent.DoesNotExist):
#             obj = None
#         if obj is None or obj.student:
#             return Response({"error": "Ссылка больше недействительна!"},
#                             status=status.HTTP_400_BAD_REQUEST)
#         # Если пользователь аутентифицирован
#         if request.user.is_authenticated:
#             if obj.email == request.user.email:
#                 obj.student = request.user.student_profile
#                 obj.save()
#             return redirect(reverse('profile'))
#         return redirect(reverse('login-with-token'))
