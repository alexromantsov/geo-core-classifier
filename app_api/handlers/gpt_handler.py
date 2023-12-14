# app_api/handlers/gpt_handler.py
import json
import asyncio
from openai import OpenAI
import os

from app_api.handlers.lithology_setting import LITHOLOGY_SETTING


class GptHandler:
    def __init__(self, request):
        self.request = request
        self.api_key = os.getenv('API_KEY')
        self.description: str
        self.model_request: str

        # OpenAI
        self.client = OpenAI(api_key=self.api_key)
        self.gpt_model = "gpt-3.5-turbo-1106"
        self.gpt_temperature = 0.2
        self.gpt_response_format = {"type": "json_object"}

    def _validation(self):
        key_description = "description"
        key_model = "model"
        data = json.loads(self.request.body)

        if not isinstance(data, dict):
            raise ValueError("Некорректный формат данных: ожидался JSON-объект.")

        # Проверка наличия ключа 'description'
        if key_description not in data:
            raise ValueError(f"Отсутствует ключ '{key_description}'.")

        # Проверка типа значения ключа 'description'
        if not isinstance(data['description'], str):
            raise ValueError(f"Некорректный тип данных для ключа '{key_description}': ожидалась строка.")

        # # Проверка наличия ключа 'model'
        # if key_model not in data:
        #     raise ValueError(f"Отсутствует ключ '{key_model}'.")
        #
        # # Проверка типа значения ключа 'model'
        # if not isinstance(data['model'], str):
        #     raise ValueError(f"Некорректный тип данных для ключа '{key_model}': ожидалась строка.")

        self.description = data['description']

    def _validation_response(self, response_data):
        data = json.loads(response_data)

        if not isinstance(data, dict):
            raise ValueError("Некорректный формат данных: GPT вернул не JSON-объект.")

        code = data.get("code")
        message = data.get("message", "success")
        response_content = {}

        # Проверка кода ответа
        if code == 200 or code == "200" or code is None:
            # Проверка наличия и типов ключей для успешного ответа
            required_keys = {
                "lithotype": str,
                "structure": list,
                "color": list,
                "features": list
            }

            for key, expected_type in required_keys.items():
                if key not in data:
                    raise ValueError(f"Отсутствует ключ '{key}'.")
                if not isinstance(data[key], expected_type):
                    raise ValueError(f"Некорректный тип для ключа '{key}': ожидался {expected_type.__name__}.")
                response_content[key] = data[key]
            code = "200"

        elif code == 500 or code == "500":
            # Обработка случая, когда текст не является описанием породы
            code = "500"
            message = "Текст не является описанием породы"

        else:
            # Обработка непредвиденных кодов ответа
            raise ValueError("GPT вернул непредвиденный код ответа.")

        return {
            "code": code,
            "message": message,
            "data": response_content
        }

    def create_request_messages(self, user_message):
        system_messages = [
            "Вы являетесь высококлассным специалистом по литологическому описанию пород, который отвечает на русском языке. ",
            "Ответ должен быть представлен в строгом формате JSON. ",
            "Пример JSON: {'lithotype': '...', 'structure': [...], 'color': [...], 'features': [...] }. ",
            "При успешном ответе добавить ключ 'code' 200, если переданный текст не является описанием породы, то вернуть 'code' 500. ",
            "Если 'code' равен 200, то ключи lithotype, structure, color и features обязательно должны быть в ответе, хоть и спустым значением. ",
            f"Также при ответе в ключ 'lithotype' используй в приоритете этот список [{', '.join(LITHOLOGY_SETTING)}]. ",
            "Все параметры записывай с большой буквы. "
        ]

        # Формирование списка сообщений
        messages = [{"role": "system", "content": msg} for msg in system_messages]
        messages.append({"role": "user", "content": user_message})

        return messages

    async def send_request(self, user_message):
        messages = self.create_request_messages(user_message)

        response = await asyncio.to_thread(
            self.client.chat.completions.create,
            model="gpt-3.5-turbo-1106",
            temperature=0.2,
            response_format={"type": "json_object"},
            messages=messages
        )
        return response.choices[0].message.content

    async def run(self):
        self._validation()
        response_data = await self.send_request(self.description)
        print(response_data)
        return self._validation_response(response_data)
