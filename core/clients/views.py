from django.shortcuts import render, get_object_or_404
from rest_framework.generics import RetrieveAPIView
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .services import Email
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import jwt
# Create your views here.


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