from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("", include("clients.urls")),
    # namespace='clients')), тег url во встроенном шаблоне password-reset не работает
    path("", include("chats.urls", namespace="chats")),
    path("", include("lessons.urls", namespace="lessons")),
    path("", include("materials.urls", namespace="materials")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:

    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
