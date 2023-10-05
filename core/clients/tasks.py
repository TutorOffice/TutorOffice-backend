from celery import shared_task
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response

from .models import User


class Email:
    @staticmethod
    @shared_task
    def send_email_task(
        domain=None,
        template=None,
        email_subject=None,
        context=None,
        to_email=None,
        message=None,
        *args,
        **kwargs,
    ):
        if template:
            message = render_to_string(
                template_name=template, context={"domain": domain, **context}
            )
        email = EmailMessage(
            email_subject,
            message,
            to=[to_email],
            from_email=settings.EMAIL_HOST_USER,
        )
        email.send()
        return Response(
            {"success": "Сообщение успешно отправлено!"},
            status=status.HTTP_200_OK,
        )

    @staticmethod
    @shared_task
    def reset_password_task(subject_template_name, email_template_name, context,
                            from_email, to_email, html_email_template_name):
        context['user'] = User.objects.get(pk=context['user'])

        PasswordResetForm.send_mail(
            None,
            subject_template_name,
            email_template_name,
            context,
            from_email,
            to_email,
            html_email_template_name
        )
