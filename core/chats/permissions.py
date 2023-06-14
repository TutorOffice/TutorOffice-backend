from rest_framework.permissions import BasePermission

from clients.services import get_user_type


class IsSender(BasePermission):
    """
    Ограничение проверяющее,
    является ли пользователем отправителем
    сообщения. Проверка происходит по типу,
    т.к в чатах участвует только ученик и учитель,
    соответственно отправитель лишь один.
    """
    def has_object_permission(self, request, view, obj):
        profile = get_user_type(request)
        if profile == obj.sender:
            return True
        return False
