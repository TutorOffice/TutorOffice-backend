from __future__ import absolute_import, unicode_literals
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
# добавления переменной окружения, ссылающейся на файл настроек, нужно для celery

app = Celery('core')
# создание экземпляра класса, этот экземпляр/приложение с именем проекта - точка входа для использования celery

app.config_from_object('django.conf:settings', namespace='CELERY')
# загрузка конфигурации celery из settings, все будут иметь префикс CELERY, установка конфигов для приложения celery
# префикс означает что все параметры конфигурации в settings.py Celery должны быть заданы в верхнем регистре
# вместо нижнего, и начинаться с CELERY_


app.autodiscover_tasks()
# если используется этот параметр, значит все задачи должны находиться в файлах tasks.py
# ищет файлы tasks из всех приложений, определенных в installed_apps
# позволяет использовать shared_tasks
# shared_task decorator позволяет создавать задачи без конкретного экземпляра приложения
