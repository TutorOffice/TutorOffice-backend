from django.contrib import admin
from .models import Homework, Lesson
from clients.models import TeacherStudent


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'subject', 'show_student', 'start_time')
    date_hierarchy = 'date'
    empty_value_display = 'нет'

    def show_student(self, obj):
        return f'{obj.teacher_student.last_name} {obj.teacher_student.first_name}'
    show_student.short_description = 'Студент'


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    pass
