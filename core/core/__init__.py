from .celery import app as celery_app

__all__ = ("celery_app",)
# это доп. гарантирует, что celery приложение, которое я определил в файле celery и назвал app
# будет загружено при запуске django
