from django.contrib import admin
from .models import Material

@admin.register(Material)
class Material(admin.ModelAdmin):
    list_display = ('teacher', 'subject', 'file', 'text', 'type')
    search_fields = ('teacher',)
    list_filter = ('subject', 'type')

