from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from accounts.models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'phone_number',)
    list_filter = ('is_active', 'is_staff',)
    fieldsets = (
        (None, {'fields': ('username', 'phone_number',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_phone_confirmed',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'phone_number', 'password1', 'password2', 'is_staff', 'is_active', 'is_phone_confirmed',)
        }
         ),
    )
    search_fields = ('username', 'phone_number',)
    ordering = ('username',)


admin.site.register(CustomUser, CustomUserAdmin)
