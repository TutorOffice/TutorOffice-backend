from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from rest_framework import status
from rest_framework.response import Response


class Email:
    @staticmethod
    @shared_task
    def send_email_task(domain=None, template=None,
                        email_subject=None, context=None,
                        to_email=None, message=None, *args, **kwargs):
        if template:
            message = render_to_string(
                template_name=template,
                context={
                    'domain': domain,
                    **context
                }
            )
        email = EmailMessage(email_subject, message, to=[to_email],
                             from_email=settings.EMAIL_HOST_USER, )
        email.send()
        return Response({"success": "Сообщение успешно отправлено!"},
                        status=status.HTTP_200_OK)
