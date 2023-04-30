from rest_framework.generics import ListAPIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings

from .permissions import IsTeacher
from .serializers import *
from .services import get_user_type
from .models import User, Subject, Teacher, TeacherStudent
from .forms import CustomPasswordResetForm
from .tasks import Email

from smtplib import SMTPDataError


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
        template = 'clients/activate.html'
        email_subject = 'Подтвердите почту для активации вашего кабинета репетитора'
        to_email = user.email
        context = {
            "token": str(token),
            "full_name": f"{user.last_name} {user.first_name}"
         }
        domain = str(get_current_site(request))
        Email.send_email_task.delay(domain, template,
                                    email_subject, context,
                                    to_email)
        return Response(
            {
                "success": "Регистрация прошла успешно! "
                           "Вам было отправлено письмо "
                           "с подтверждением на почту!"
            },
            status=status.HTTP_201_CREATED
        )


class ActivateUserView(APIView):
    """Верификация почты"""

    def post(self, request, token, *args, **kwargs):
        try:
            # по refresh-токену проверяет валидность(срок) и идентифицируется пользователя
            user = User.objects.get(pk=RefreshToken(token).payload['user_id'])
        except (TokenError, User.DoesNotExist):
            user = None
        if user is None or user.is_active:
            return Response(
                {"detail": "Ссылка недействительна"},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.is_active = True
        user.save()
        refresh = RefreshToken.for_user(user)
        # добавляется тип пользователя, нужно для фронта
        request.user = user
        role = get_user_type(request)
        return Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'role': role
            },
            status=status.HTTP_200_OK
        )


class LoginView(TokenObtainPairView):
    """
    Вход, если почта не подтверждена,
    будет отправлено сообщение с подтверждением
    """

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        if email and password:
            try:
                user = User.objects.get(email=request.data['email'])
                if user.is_active:
                    response = super().post(request, *args, **kwargs)
                    # добавляется тип пользователя, нужно для фронта
                    request.user = user
                    role = get_user_type(request)
                    response.data['role'] = role
                    return response
                if user.check_password(password):
                    token = RefreshToken.for_user(user)
                    template = 'clients/activate.html'
                    email_subject = 'Подтвердите почту для активации вашего кабинета репетитора'
                    to_email = user.email
                    context = {
                        "token": str(token),
                        "full_name": f"{user.last_name} {user.first_name}"
                    }
                    domain = str(get_current_site(request))
                    Email.send_email_task.delay(domain, template, email_subject, context, to_email)
                    return Response({"detail": "Ваша почта не подтверждена! "
                                               "На неё было отправлено новое письмо с подтверждением!"},
                                    status=status.HTTP_401_UNAUTHORIZED)
                raise User.DoesNotExist
            except User.DoesNotExist:
                return Response({"detail": "Не найдено активной учетной записи с указанными данными"},
                                status=status.HTTP_400_BAD_REQUEST)
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

    def perform_create(self, serializer):
        """
        Сохраняет запись в бд, добавив внешний
        ключ на учителя
        """
        teacher = self.request.user.teacher_profile
        serializer.save(teacher=teacher)


class RelateUnrelateStudentView(APIView):
    """
    Вьюха для отправки запроса на добавление
    и отвязки ученика учителем
    """
    permission_classes = [IsAuthenticated, IsTeacher]

    def post(self, request, pk, format=None):
        """
        Отправляет запрос на добавление ученику, если он есть в базе
        запрашивает подтверждения, если ученика нет в базе, то просто предлагает
        зарегистрироваться
        """
        # получение записи из таблицы TeacherStudent по её id
        try:
            obj = TeacherStudent.objects.get(pk=pk)
        except TeacherStudent.DoesNotExist:
            return Response({"error": "Такой записи не существует!"})
        if obj.teacher.user != request.user:
            return Response({"error": "У вас нет прав на осуществление этого действия!"})
        if obj.student:
            return Response({"error": "К данной записи ученик уже привязан!"})
        email = obj.email
        # проверка наличия пользователя с такой почтой в базе
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        to_email = obj.email
        template = 'clients/relation.html'
        context = {
            "teacher_name": f"{request.user.first_name} {request.user.last_name}",
        }
        domain = str(get_current_site(request))
        # если пользователь есть в базе, отправляется ссылка на подтверждение
        if user:
            try:
                student_profile = user.student_profile
            except Student.DoesNotExist:
                return Response({"error": "Вы не можете добавить этого пользователя, "
                                          "так как он не является учеником!"})
            email_subject = 'Подтвердите запрос от репетитора!'
            context['student_name'] = f"{user.last_name} {user.first_name}"
            context['url_name'] = 'confirm'
            # !Нужно будет изменить имя на то, что будет определено в сеттингс
            # токен будет использоваться в ссылке, для связи записей ученика и TeacherStudent
            token = RefreshToken.for_user(obj)
            token['student'] = student_profile.id
            context['token'] = str(token)
        # если пользователя нет в базе, отправляется запрос на регистрацию
        else:
            email_subject = 'Зарегистрируйтесь и подтвердите запрос от репетитора!'
            context['url_name'] = 'register-list'
            # !Нужно будет изменить имя на то, что будет определено в сеттингс
        try:
            Email.send_email_task.delay(domain, template, email_subject, context, to_email)
        except SMTPDataError:
            return Response({"error": "Почта не найдена! "
                            "Невозможно отправить сообщение для подтверждения!"},
                            status=status.HTTP_400_BAD_REQUEST)
        obj.bind = 'awaiting'
        obj.save()
        return Response({"success": "Ваш запрос был успешно отправлен на почту пользователю!"},
                        status=status.HTTP_200_OK)

    def patch(self, request, pk, format=None):
        """Метод для отвязки ученика от учителя"""
        try:
            obj = TeacherStudent.objects.get(pk=pk)
        except TeacherStudent.DoesNotExist:
            return Response({"error": "Такой записи не существует!"})
        if obj.teacher.user != request.user:
            return Response({"error": "У вас нет прав на осуществление этого действия!"})
        if not obj.student:
            return Response({"error": "К этой записи не привязан ученик!"})
        obj.student = None
        obj.bind = 'unrelated'
        obj.save()
        return Response({"success": "Ученик был успешно отвязан от вас!"})


class ConfirmView(APIView):
    """Подтверждение учеником привязки к репетитору"""
    def get(self, request, token):
        try:
            obj = TeacherStudent.objects.get(pk=RefreshToken(token).payload['user_id'])
        except (TokenError, TeacherStudent.DoesNotExist):
            obj = None
        if obj is None or obj.student:
            return Response({"error": "Ссылка больше недействительна!"},
                            status=status.HTTP_400_BAD_REQUEST)
        student_id = RefreshToken(token).payload['student']
        student = Student.objects.get(pk=student_id)
        obj.student = student
        obj.bind = 'related'
        obj.save()
        # Отправка уведомления учителю о добавлении
        send_mail(
            subject='Ученик подтвердил запрос на добавление!',
            message=(f'Пользователь {obj.last_name} {obj.first_name} подтвердил'
                     f'запрос на его добавление в качестве ученика!'),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[obj.teacher.user.email],
            fail_silently=False,
        )
        return Response({"success": "Вы были успешно добавлены к репетитору!"},
                        status=status.HTTP_200_OK)
