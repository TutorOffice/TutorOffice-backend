from django.contrib import admin
from .models import Homework, Lesson


class HomeworkAdmin(admin.StackedInline):
    model = Homework
    list_display = ('show_teacher', 'lesson', 'title')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'subject', 'date', 'show_student', 'start_time', 'show_homework')
    date_hierarchy = 'date'
    inlines = [HomeworkAdmin]

    def show_student(self, obj):
        return (
            f'{obj.teacher_student.last_name} {obj.teacher_student.first_name}'
        )
    show_student.short_description = 'Студент'

    @admin.display(boolean=True)
    def show_homework(self, obj):
        return Homework.objects.filter(lesson=obj).exists()
    show_homework.short_description = 'Домашнее задание'

