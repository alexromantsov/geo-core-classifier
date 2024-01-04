# app_db/urls.py
from django.urls import path
from app_api.views import GptApiView
from .views import random_core_description, handle_excel_file

app_name = 'app_db'

urlpatterns = [
    path('gpt', GptApiView.as_view(), name='gpt-api'),
    path('random-description', random_core_description, name='random-core-description'),
    path('upload-excel', handle_excel_file, name='upload-excel'),
]
