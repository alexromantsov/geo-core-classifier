from django.db import models

from server import settings


class UserAction(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Имя",
        blank=True,
        null=True
    )
    surname = models.CharField(
        max_length=100,
        verbose_name="Фамилия",
        blank=True,
        null=True
    )
    ip_address = models.GenericIPAddressField(
        verbose_name="IP адрес"
    )
    group = models.CharField(
        max_length=50,
        choices=settings.USER_GROUPS,
        default='undefined',  # По умолчанию - Неопределенный пользователь
        verbose_name="Группа"
    )
    available_requests = models.IntegerField(
        verbose_name="Доступно запросов",
        blank=True,
        null=True
    )
    total_clicks = models.IntegerField(
        verbose_name="Всего кликов",
        blank=True,
        null=True
    )
    action_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время действия"
    )

    def __str__(self):
        if self.name and self.surname:
            return f"{self.name} {self.surname} - {self.ip_address}"
        else:
            return self.ip_address

    class Meta:
        verbose_name = "Действие пользователя"
        verbose_name_plural = "Действия пользователей"
