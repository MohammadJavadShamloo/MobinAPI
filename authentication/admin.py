from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Token, ArchPic


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'user_agent',)
    list_filter = ('user_agent', )


@admin.register(ArchPic)
class ArchPicAdmin(admin.ModelAdmin):
    list_display = ('title',)