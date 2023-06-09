from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ChatViewSet

app_name = "chats"

router = DefaultRouter()
router.register(
    r"chats", ChatViewSet, basename="chats"
)
urlpatterns = [path("", include(router.urls))]
