# app_db/handlers/core_description_example.py
from ..models.core_description_example import CoreDescriptionExample
from django.utils import timezone


class CoreDescriptionExampleHandler:

    @staticmethod
    def create_description(description, language='en'):
        """Создает новое описание керна."""
        # Проверка на существование такого же описания на том же языке
        if CoreDescriptionExample.objects.filter(description=description, language=language).exists():
            return None

        example = CoreDescriptionExample(
            description=description,
            language=language,
            created_at=timezone.now()
        )
        example.save()
        return example


    @staticmethod
    def get_description(description_id):
        """Возвращает описание керна по ID."""
        return CoreDescriptionExample.objects.get(id=description_id)

    @staticmethod
    def get_description_by_description(text_description):
        """Возвращает описание керна по текстовому описанию."""
        try:
            return CoreDescriptionExample.objects.filter(description__icontains=text_description).first()
        except CoreDescriptionExample.DoesNotExist:
            return None

    @staticmethod
    def get_description_by_language(language):
        """Возвращает описание керна по языку."""
        try:
            return CoreDescriptionExample.objects.filter(language=language).first()
        except CoreDescriptionExample.DoesNotExist:
            return None

    @staticmethod
    def update_description(description_id, **kwargs):
        """Обновляет описание керна."""
        example = CoreDescriptionExample.objects.get(id=description_id)
        for key, value in kwargs.items():
            setattr(example, key, value)
        example.save()
        return example

    @staticmethod
    def delete_description(description_id):
        """Удаляет описание керна."""
        example = CoreDescriptionExample.objects.get(id=description_id)
        example.delete()
