from rest_framework.permissions import BasePermission


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

class IsAdministrator(BasePermission):
    """Разрешения для пользователя с ролью
     администратор или суперпользователь."""
    def has_permission(self, request, view):
        return (request.user.is_superuser
                or request.user.is_staff)


class IsTeacherOwnerOrIsStaffPermission(BasePermission):
    """Разрешение на редактирование учителю(владельцу) и персоналу."""
    def has_object_permission(self, request, view, obj):
        return (obj.teacher.user == request.user
                or request.user.is_staff
                or request.user.is_superuser)
