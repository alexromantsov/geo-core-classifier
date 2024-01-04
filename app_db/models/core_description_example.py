# app_db/models/core_description_example.py
from django.db import models
from django.conf.global_settings import LANGUAGES


class CoreDescriptionExample(models.Model):
    description = models.TextField(
        verbose_name="Описание керна"
    )
    language = models.CharField(
        max_length=100,
        choices=LANGUAGES,
        verbose_name="Язык"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания"
    )

    def __str__(self):
        return f"Описание керна на {self.language} от {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

    class Meta:
        verbose_name = "Описание керна"
        verbose_name_plural = "Описания кернов (примеры)"
