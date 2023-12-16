# app_db/models/core_response.py
from django.db import models
from django.db.models import JSONField


class CoreResponse(models.Model):
    core_description = models.TextField(
        verbose_name="Описание керна"
    )
    response_data = JSONField(
        verbose_name="Данные ответа"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания"
    )

    def __str__(self):
        return f"Ответ на запрос от {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

    class Meta:
        verbose_name = "Ответ на запрос"
        verbose_name_plural = "Ответы на запросы"
