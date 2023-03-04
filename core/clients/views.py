from django.shortcuts import render, get_object_or_404
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import User
from .serializers import RegisterSerializer
from .services import Email
import jwt
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.


class RegisterView(CreateAPIView, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class SendEmailView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['uid'])
        token = RefreshToken.for_user(user)
        response = Email.send_email(request, user, token)
        return response


class ActivateUserView(RetrieveAPIView):

    def get(self, request, token, *args, **kwargs):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.algorithms)
            user = get_object_or_404(User, pk=payload['user_id'])
            if not user.is_active:
                user.is_active = True
                user.save()
                return Response({"SUCCESS": "Аккаунт успешно активирован!",
                                 "user_id": user.id},
                                 status=status.HTTP_200_OK)
                # Возврат refresh-токена?
            return Response({"ERROR": "Ссылка больше недействительна!"},
                            status=status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError as error:
            return Response({'ERROR': "Срок действия ссылки для активации истёк!"},
                            status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as error:
            return Response({'ERROR': "Неверная ссылка!"},
                            status=status.HTTP_400_BAD_REQUEST)

