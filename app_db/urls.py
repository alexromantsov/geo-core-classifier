# app_db/urls.py
from django.urls import path

from app_api.views import GptApiView

urlpatterns = [
    path('gpt', GptApiView.as_view(), name='gpt-api'),
    # Другие маршруты вашего приложения app_db
]
