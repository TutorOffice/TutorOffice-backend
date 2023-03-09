from django.contrib import admin
from .models import Homework, Lesson
from clients.models import TeacherStudent


class TeacherStudentInLine(admin.StackedInline):
    model = TeacherStudent
    extra = 1

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    pass
