from django.contrib import admin

from .models import Material


@admin.register(Material)
class Material(admin.ModelAdmin):
    list_display = (
        "id", "date", "teacher", "material_type", "show_students", "subject", "file",
    )
    list_display_links = ("id", "teacher",)
    list_filter = ("subject", "material_type", "date",)
    search_fields = ("teacher",)
    empty_value_display = "-пусто-"

    def show_students(self, obj):
        return [
            f"{item.last_name} {item.first_name}" for item in obj.teacher_student.all()
        ]

    show_students.short_description = "Ученики"