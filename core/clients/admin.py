from django.contrib import admin
from .models import User, Subject, Teacher, Student, TeacherStudent


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'show_full_name', 'phone',
                    'is_active', 'show_student', 'show_teacher')
    search_fields = ('last_name', 'phone', 'email')
    search_help_text = ('Фамилия, телефон или e-mail')
    list_filter = ('is_active', 'is_staff',)
    empty_value_display = '-пусто-'

    def show_full_name(self, obj):
        return f'{obj.last_name} {obj.first_name}'
    show_full_name.short_description = 'ФИО'

    @admin.display(boolean=True)
    def show_student(self, obj):
        return Student.objects.filter(user=obj).exists()
    show_student.short_description = 'Студент'

    @admin.display(boolean=True)
    def show_teacher(self, obj):
        return Teacher.objects.filter(user=obj).exists()
    show_teacher.short_description = 'Учитель'


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'show_email',
                    'show_phone', 'show_is_active')
    search_fields = ('user__last_name', 'user__email', 'user__phone')
    search_help_text = ('Фамилия, почта или телефон')

    def show_email(self, obj):
        return obj.user.email
    show_email.short_description = 'Электронная почта'

    def show_phone(self, obj):
        return obj.user.phone
    show_phone.short_description = 'Телефон'

    @admin.display(boolean=True)
    def show_is_active(self, obj):
        return obj.user.is_active
    show_is_active.short_description = 'Подтвержден'


@admin.register(Teacher)
class TeachertAdmin(admin.ModelAdmin):
    list_display = ('user', 'show_subjects', 'show_students')
    search_fields = ('user__last_name', 'user__email', 'user__phone')
    search_help_text = ('Фамилия, почта или телефон учителя')

    def show_subjects(self, obj):
        subject_list = []
        for subject in obj.subjects.all():
            subject_list.append(subject.title)
        return ', '.join(subject_list)
    show_subjects.short_description = 'Предметы'

    def show_students(self, obj):
        student_list = []
        queryset_students = TeacherStudent.objects.filter(teacher=obj)
        for _ in queryset_students:
            student_list.append(f'{_.last_name} {_.first_name}')
        return ', '.join(student_list)
    show_students.short_description = 'Студенты'


@admin.register(TeacherStudent)
class TeacherStudentAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'show_student', 'email', 'verify')

    def show_student(self, obj):
        return f'{obj.last_name} {obj.first_name}'
    show_student.short_description = 'Студент'
