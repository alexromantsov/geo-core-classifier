# app_db/admin.py
from django.contrib import admin
from .models.user_action import UserAction
from .models.core_response import CoreResponse
from .models.core_description_example import CoreDescriptionExample


@admin.register(UserAction)
class UserActionAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'ip_address', 'group', 'available_requests', 'total_clicks', 'action_time')
    list_filter = ('group',)
    search_fields = ('name', 'surname', 'ip_address')


@admin.register(CoreResponse)
class CoreResponseAdmin(admin.ModelAdmin):
    list_display = ('core_description', 'created_at')
    search_fields = ('core_description',)

@admin.register(CoreDescriptionExample)
class CoreDescriptionExampleAdmin(admin.ModelAdmin):
    list_display = ('description', 'language', 'created_at')
    list_filter = ('language',)
    search_fields = ('description',)
