from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('clients.urls')),
    path('', include('lessons.urls')),
    path('', include('materials.urls'))
]

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
    ]
