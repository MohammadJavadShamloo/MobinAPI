from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Token


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'user_agent',)
