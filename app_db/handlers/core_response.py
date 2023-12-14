# app_db/handlers/core_response.py
from ..models.core_response import CoreResponse
from django.utils import timezone


class CoreResponseHandler:

    @staticmethod
    def create_response(core_description, response_data):
        """Создает новый ответ."""
        response = CoreResponse(
            core_description=core_description,
            response_data=response_data,
            created_at=timezone.now()
        )
        response.save()
        return response

    @staticmethod
    def get_response(response_id):
        """Возвращает ответ по ID."""
        return CoreResponse.objects.get(id=response_id)

    @staticmethod
    def get_response_by_description(core_description):
        """Возвращает ответ по описанию."""
        try:
            return CoreResponse.objects.filter(core_description=core_description).first()
        except CoreResponse.DoesNotExist:
            return None

    @staticmethod
    def update_response(response_id, **kwargs):
        """Обновляет ответ."""
        response = CoreResponse.objects.get(id=response_id)
        for key, value in kwargs.items():
            setattr(response, key, value)
        response.save()
        return response

    @staticmethod
    def delete_response(response_id):
        """Удаляет ответ."""
        response = CoreResponse.objects.get(id=response_id)
        response.delete()
