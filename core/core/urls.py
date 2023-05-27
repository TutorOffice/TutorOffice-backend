from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('clients.urls', namespace='clients')),
    path('', include('lessons.urls', namespace='lessons')),
    path('', include('materials.urls', namespace='materials')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    from rest_framework import permissions
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi

    schema_view = get_schema_view(
        openapi.Info(
            title="TutorOffice API",
            default_version='v1',
        ),
        public=True,
        permission_classes=[permissions.AllowAny],
    )
    urlpatterns += [
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
        path('__debug__/', include('debug_toolbar.urls')),
    ]
