from django.contrib import admin
from .models.user_action import UserAction


@admin.register(UserAction)
class UserActionAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'ip_address', 'group', 'available_requests', 'total_clicks', 'action_time')
    list_filter = ('group',)
    search_fields = ('name', 'surname', 'ip_address')
