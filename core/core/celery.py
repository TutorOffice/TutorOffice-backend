from celery import Celery

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clients.settings')
# установка стандартных настроек Django ля Celery

app = Celery('clients')
# создание приложения

