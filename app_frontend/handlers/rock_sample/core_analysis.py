import json

from app_db.handlers.user_action import UserActionHandler


class CoreAnalysis:
    def __init__(self, request):
        self.request = request
        self.user_ip = self.get_client_ip()
        self.user_action = UserActionHandler.get_or_create_action_by_ip(self.user_ip)
        self.user_id = self.user_action.id
        self.available_requests = self.user_action.available_requests
        self.core_description: str
        self.model: str

    def _validation(self):
        data = json.loads(self.request.body)
        if isinstance(data, dict):
            if isinstance(data.get("description"), str):
                core_description = data.get("description")
                if core_description == "":
                    raise ValueError("Поле с описанием керна пустое...")
                self.core_description = core_description

            if isinstance(data.get("model"), str):
                model = data.get("model")
                if model == "":
                    raise ValueError("Необходимо выбрать модель обработки...")
                self.model = model

    def run(self):
        # Валидация входных данных
        self._validation()

        # Уменьшаем количество доступных запросов
        if self.available_requests is not None:
            self.available_requests -= 1
            self.user_action.available_requests = self.available_requests
            self.user_action.save()


        return {
            "code": "200",
            "message": "Анализ выполнен",
            "data": {
                "available_requests": self.available_requests
            }
        }

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip
