from rest_framework.permissions import BasePermission

from clients.services import get_user_type


class IsTeacher(BasePermission):
    """
    Кастомное ограничение прав доступа, проверяющее
    является ли пользователь репетитором (имеет профиль)
    """

    def has_permission(self, request, view):
        profile = get_user_type(request)
        if profile == "teacher":
            return True
        return False


class IsTeacherOwner(IsTeacher):
    """
    Ограничение проверяет, относится ли
    этот репетитор к уроку или материалу
    """

    def has_object_permission(self, request, view, obj):
        if request.user == obj.teacher.user:
            return True
        return False


class IsStudent(BasePermission):
    """
    Кастомное ограничение прав доступа, проверяющее
    является ли пользователь студентом (имеет профиль)
    """

    def has_permission(self, request, view):
        profile = get_user_type(request)
        if profile == "student":
            return True
        return False


class IsStudentOwner(IsStudent):
    """
    Ограничение проверяет, относится ли
    этот ученик к уроку
    """

    def has_object_permission(self, request, view, obj):
        if request.user.student_profile == obj.teacher_student.student:
            return True
        return False
