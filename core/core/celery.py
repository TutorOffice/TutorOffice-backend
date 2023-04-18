from __future__ import absolute_import, unicode_literals
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
# создание переменной окружения с настройками django, требуется для celery,

app = Celery('core')
# создание экземпляра celery с именем core
app.config_from_object('django.conf:settings', namespace='CELERY')
# загрузка конфигурации celery из settings, все будут иметь префикс CELERY

# отключает использование utc


app.autodiscover_tasks()
# автоматически обнаруживает и регистрирует задачи (функции, которые должны быть выполнены асинхронно)
# ищет таски из приложений, определнных в installed_apps
