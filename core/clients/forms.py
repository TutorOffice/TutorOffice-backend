from django.contrib.auth.forms import PasswordResetForm
from .tasks import Email

from .models import User


class CustomPasswordResetForm(PasswordResetForm):
    """
    Форма для сброса пароля, которая отвечает также
    за поиск пользователя по введённой почте.
    """

    # Переписан метод получения пользователей. Удаляется
    # требование получать только активных, т.к пользователи
    # которые, только зарегистрировались активными до
    # подтверждения почты не являются. И если они не подтвердили
    # аккаунт сразу и забыли пароль (А ссылка для подтверждения имеет
    # срок годности), то они не смогут его восстановить
    # Это решение позволяет избежать проблемы
    def get_users(self, email):
        """
        Метод получения пользователя по
        введенной почте, удаляется требование
        искать пользователей только среди активных.
        """
        return User.objects.filter(email__iexact=email)

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        context['user'] = context['user'].id

        Email.send_email_task.delay(
            subject_template_name=subject_template_name,
            email_template_name=email_template_name,
            context=context,
            from_email=from_email,
            to_email=to_email,
            html_email_template_name=html_email_template_name
        )
