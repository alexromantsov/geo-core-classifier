# app_db/management/commands/generate_core_descriptions.py
from django.core.management.base import BaseCommand
from app_db.handlers.core_description_example import CoreDescriptionExampleHandler
from .test_descriptions import TEST_DESCRIPTIONS

class Command(BaseCommand):
    help = 'Генерирует тестовые описания керна'

    def handle(self, *args, **kwargs):
        try:
            for language, description in TEST_DESCRIPTIONS:
                # Создание тестового описания
                created_description = CoreDescriptionExampleHandler.create_description(description, language)
                if created_description:
                    self.stdout.write(self.style.SUCCESS(f' + Успешно создано описание: "{description}" на языке {language}'))
                else:
                    self.stdout.write(self.style.WARNING(f' - Не удалось создать описание: "{description}" на языке {language}'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f' ! Произошла ошибка при создании описаний: {e}'))
