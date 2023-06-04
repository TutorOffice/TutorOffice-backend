from django.contrib import admin

from .models import Material


@admin.register(Material)
class Material(admin.ModelAdmin):
    list_display = ("teacher", "subject", "file", "material_type",)
    list_filter = ("subject", "material_type",)
    search_fields = ("teacher",)
