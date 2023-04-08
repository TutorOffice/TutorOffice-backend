from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from rest_framework import status
from rest_framework.response import Response


class Email:
    @staticmethod
    def send_email(request, template, email_subject, context, to_email):
        domain = get_current_site(request)
        message = render_to_string(
            template_name=template,
            context={
                'domain': domain,
                **context
            })
        email = EmailMessage(email_subject, message, to=[to_email],
                             from_email=settings.EMAIL_HOST_USER)
        email.send()
        return Response({"success": "Сообщение успешно отправлено!"},
                        status=status.HTTP_200_OK)
