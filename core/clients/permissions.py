from rest_framework.permissions import BasePermission
from .services import get_user_type


class IsTeacher(BasePermission):
    """
    Кастомное ограничение прав доступа, проверяющее
    является ли пользователь учителем (имеет профиль)
    """
    def has_permission(self, request, view):
        profile = get_user_type(request)
        if profile == 'teacher':
            return True
        return False


class IsTeacherOwner(BasePermission):
    """
    Ограничение проверяет, является ли
    этот учитель владельцем записи
    """
    def has_object_permission(self, request, view, obj):
        if request.user == obj.teacher.user:
            return True
        return False


class IsStudentOwner(BasePermission):
    """
    Ограничение проверяет, относится ли
    этот ученик к записи урока
    """
    def has_permission(self, request, view):
        profile = get_user_type(request)
        if profile == 'student':
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.student_profile == obj.teacher_student.student:
            return True
        return False


class IsStud(BasePermission):
    """
    Ограничение проверяет, относится ли
    этот ученик к записи ученика репетитора
    """
    def has_permission(self, request, view):
        profile = get_user_type(request)
        if profile == 'student':
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.student_profile == obj.student:
            return True
        return False
