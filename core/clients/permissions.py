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

class IsAdministrator(BasePermission):
    """Разрешения для пользователя с ролью
     администратор или суперпользователь."""
    def has_permission(self, request, view):
        return (request.user.is_superuser
                or request.user.is_staff)


class IsTeacherOwnerOrIsStaffPermission(BasePermission):
    """Разрешение на редактирование учителю(владельцу) и персоналу,
    остальным пользователям только просмотр"""
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.teacher.user == request.user
                or request.user.is_staff
                or request.user.is_superuser)
