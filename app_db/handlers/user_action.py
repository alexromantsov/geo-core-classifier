# app_db/handlers/user_action.py
from ..models.user_action import UserAction
from django.utils import timezone


class UserActionHandler:

    @staticmethod
    def create_action(ip_address, group, name=None, surname=None, available_requests=None, total_clicks=None):
        """Создает новое действие пользователя."""
        action = UserAction(
            name=name,
            surname=surname,
            ip_address=ip_address,
            group=group,
            available_requests=available_requests,
            total_clicks=total_clicks,
            action_time=timezone.now()
        )
        action.save()
        return action

    @staticmethod
    def get_action(action_id):
        """Возвращает действие пользователя по ID."""
        return UserAction.objects.get(id=action_id)

    @staticmethod
    def get_action_by_ip(ip_address):
        """Возвращает действие пользователя по IP-адресу."""
        try:
            return UserAction.objects.get(ip_address=ip_address)
        except UserAction.DoesNotExist:
            return None

    @staticmethod
    def update_action(action_id, **kwargs):
        """Обновляет действие пользователя."""
        action = UserAction.objects.get(id=action_id)
        for key, value in kwargs.items():
            setattr(action, key, value)
        action.save()
        return action

    @staticmethod
    def delete_action(action_id):
        """Удаляет действие пользователя."""
        action = UserAction.objects.get(id=action_id)
        action.delete()

    @staticmethod
    def get_or_create_action_by_ip(
            ip_address,
            group='undefined',
            name=None,
            surname=None,
            available_requests=5,
            total_clicks=0
    ):
        """Получает или создает действие пользователя по IP-адресу."""
        action, created = UserAction.objects.get_or_create(
            ip_address=ip_address,
            defaults={
                'name': name,
                'surname': surname,
                'group': group,
                'available_requests': available_requests,
                'total_clicks': total_clicks,
                'action_time': timezone.now()
            }
        )
        return action
