from django.contrib import admin
from .models import Material

@admin.register(Material)
class Material(admin.ModelAdmin):
    list_display = ('teacher', 'subject', 'file', 'type')
    list_filter = ('subject', 'type')
    search_fields = ('teacher',)

