from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from smtplib import SMTPDataError
from rest_framework.response import Response
from rest_framework import status


class Email:
    @staticmethod
    def send_email(request, user, token):
        domain = get_current_site(request)
        email_subject = 'Подтвердите почту для активации вашего кабинета репетитора'
        message = render_to_string('clients/activate.html',
                                   {'full_name': f"{user.last_name} {user.first_name}",
                                    'domain': domain,
                                    'token': token})
        to_email = user.email
        email = EmailMessage(email_subject, message, to=[to_email],
                             from_email=settings.EMAIL_HOST_USER)
        email.send()
        return Response({"info": "Для доступа в личный кабинет вам необходимо подтвердить почту! "
                         "Сообщение с вложенной ссылкой уже было отправлено вам!"},
                        status=status.HTTP_200_OK)

    @staticmethod
    def send_to_anonuser(request, email, token):
        domain = get_current_site(request)
        email_subject = 'Зарегистрируйтесь и подтвердите запрос от репетитора!'
        message = render_to_string('clients/anonuser.html',
                                   {'domain': domain,
                                    'token': token})
        to_email = email
        email = EmailMessage(email_subject, message, to=[to_email],
                             from_email=settings.EMAIL_HOST_USER)
        email.send()
        return Response({"info": "Сообщение пользователю по указанной вами почте успешно отправлено!"},
                        status=status.HTTP_200_OK)
