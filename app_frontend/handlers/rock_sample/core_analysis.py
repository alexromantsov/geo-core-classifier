# app_frontend/handlers/rock_sample/core_analysis.py
import asyncio
import json
import re

from django.http import HttpRequest

from app_api.handlers.gpt_handler import GptHandler
from app_db.handlers.core_response import CoreResponseHandler
from app_db.handlers.user_action import UserActionHandler
from server.settings import USER_UNDEFINED, USER_PRO, USER_ADMIN

MODEL_STANDARD = 'standard'
MODEL_STANDARD_PLUS = 'standard_plus'


class MockHttpRequest(HttpRequest):
    def __init__(self, method, body):
        super().__init__()
        self.method = method
        self._body = body

    @property
    def body(self):
        return self._body



class CoreAnalysis:
    def __init__(self, request):
        self.request = request
        self.user_ip = self.get_client_ip()
        self.user_action = UserActionHandler.get_or_create_action_by_ip(self.user_ip)
        self.user_id = self.user_action.id
        self.user_group = self.user_action.group
        self.available_requests = self.user_action.available_requests
        self.total_clicks = self.user_action.total_clicks
        self.core_description: str
        self.model: str

    def _validate_language(self, text):
        """Определяет язык текста и проверяет, что он на русском или английском."""
        russian_chars = len(re.findall('[а-яА-Я]', text))
        english_chars = len(re.findall('[a-zA-Z]', text))
        total_chars = len(text)

        russian_percent = (russian_chars / total_chars) * 100 if total_chars > 0 else 0
        english_percent = (english_chars / total_chars) * 100 if total_chars > 0 else 0

        # print(f"russian_percent: {russian_percent}")
        # print(f"english_percent: {english_percent}")

        # Нужно из расчета убрать цифры, символы и пробелы

        # Пороговые значения для определения языка
        threshold = 55  # Процент для определения доминирующего языка
        if russian_percent > threshold:
            return "Russian"
        elif english_percent > threshold:
            return "English"
        else:
            return "Other"

    def _validation(self):
        data = json.loads(self.request.body)
        if isinstance(data, dict):
            if isinstance(data.get("description"), str):
                core_description = data.get("description")
                if core_description == "":
                    raise ValueError("Поле с описанием керна пустое...")

                # Проверка количества слов для пользователей с неопределенной группой
                if len(core_description.split()) > 25 and self.user_group == USER_UNDEFINED:
                    raise ValueError("Большие запросы доступны только в PRO версии. \n"
                                     "Ограничьте запрос до 25 слов.")

                # Общая проверка количества слов для всех пользователей
                if len(core_description.split()) > 300:
                    raise ValueError("Запрос не должен превышать 300 слов.")

                # Проверка языка
                language = self._validate_language(core_description)
                if language == "Other":
                    raise ValueError("Обрабатываю только русский или английский язык.")

                self.core_description = core_description

            if isinstance(data.get("model"), str):
                model = data.get("model")
                if model == "":
                    raise ValueError("Необходимо выбрать модель обработки...")
                self.model = model

    def _update_user_action(self):
        """Уменьшение количества доступных запросов и обновление общего количества кликов."""
        if self.available_requests is not None:
            # Уменьшаем количество доступных запросов в зависимости от модели
            if self.model == MODEL_STANDARD:
                self.available_requests -= 1
            elif self.model == MODEL_STANDARD_PLUS:
                self.available_requests -= 2
            else:
                self.available_requests -= 1

            self.total_clicks += 1
            self.user_action.available_requests = self.available_requests
            self.user_action.total_clicks = self.total_clicks
            self.user_action.save()

    def _filter_response_data(self, response_data):
        """Фильтрует response_data в соответствии с self.model."""
        if self.model == MODEL_STANDARD:
            allowed_keys = ['lithotype', 'color']
        else:  # Если self.model не 'standard', предполагаем что это 'extended'
            allowed_keys = ['lithotype', 'color', 'structure', 'features']

        return {key: response_data[key] for key in allowed_keys if key in response_data}

    def run(self):
        # Валидация входных данных
        self._validation()
        response_data = {}
        message_text = "Упс, что-то пошло не так..."
        status_code = "501"

        # Проверяем в БД нет ли такого self.core_description
        existing_response = CoreResponseHandler.get_response_by_description(self.core_description)
        if existing_response:
            response_gpt = existing_response.response_data
            response_data = response_gpt.get("data")

        else:
            # Создание псевдо-запроса
            body_data = json.dumps({
                "description": self.core_description,
                "model": self.model
            })
            pseudo_request = MockHttpRequest('POST', body_data)

            # Использование GptHandler с псевдо-запросом
            gpt_handler = GptHandler(pseudo_request)
            response_gpt = asyncio.run(gpt_handler.run())

            # Сохраняем запрос в БД
            CoreResponseHandler.create_response(
                self.core_description,
                response_gpt
            )

            response_data = response_gpt.get("data")



        # Фильтрация response_data
        filtered_response_data = self._filter_response_data(response_data)

        if not filtered_response_data == {}:
            # Обновление данных пользователя
            self._update_user_action()
            message_text = "Анализ выполнен"
            status_code = "200"

        return {
            "code": status_code,
            "message": message_text,
            "data": {
                "available_requests": self.available_requests,
                "response_data": filtered_response_data
            }
        }

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

