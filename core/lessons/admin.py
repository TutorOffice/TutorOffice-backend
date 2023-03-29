from django.contrib import admin

from .models import Homework, Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'subject', 'date', 'show_student', 'start_time')
    date_hierarchy = 'date'

    def show_student(self, obj):
        return (
            f'{obj.teacher_student.last_name} {obj.teacher_student.first_name}'
        )
    show_student.short_description = 'Студенты'

#    def formfield_for_foreignkey(self, db_field, request, **kwargs):
#        if db_field.name == "teacher_student":
#            kwargs["queryset"] = TeacherStudent.objects.filter(teacher=2)
#       return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'title')
