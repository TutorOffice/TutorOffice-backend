from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsTeacher(BasePermission):
    """
    Кастомное ограничение прав доступа, проверяющее
    является ли пользователь учителем (имеет профиль)
    """
    def has_permission(self, request, view):
        try:
            return request.user.teacher_profile is not None
        except AttributeError:
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
    этот ученик к записи
    """
    def has_object_permission(self, request, view, obj):
        print(request.user.student_profile)
        print(obj.teacher_student.student)
        if request.user.student_profile == obj.teacher_student.student:
            return True
        return False
