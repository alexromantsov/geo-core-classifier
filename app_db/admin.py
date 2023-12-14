from django.contrib import admin
from .models.user_action import UserAction
from .models.core_response import CoreResponse


@admin.register(UserAction)
class UserActionAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'ip_address', 'group', 'available_requests', 'total_clicks', 'action_time')
    list_filter = ('group',)
    search_fields = ('name', 'surname', 'ip_address')


@admin.register(CoreResponse)
class CoreResponseAdmin(admin.ModelAdmin):
    list_display = ('core_description', 'created_at')
    search_fields = ('core_description',)
