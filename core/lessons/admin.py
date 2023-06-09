from django.contrib import admin

from .models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "teacher",
        "subject",
        "show_student",
        "date",
        "start_time",
        "status",
    )
    list_display_links = ("id", "teacher")
    date_hierarchy = "date"
    empty_value_display = "-пусто-"

    def show_student(self, obj):
        return (
            f"{obj.teacher_student.last_name} {obj.teacher_student.first_name}"
        )

    show_student.short_description = "Ученик"
