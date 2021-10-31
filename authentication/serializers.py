from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from .utils import IranPhoneNumberValidator, PasswordValidator


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, validators=(UnicodeUsernameValidator,))
    phone_number = serializers.CharField(max_length=11, validators=(IranPhoneNumberValidator,))
    password1 = serializers.CharField(validators=(PasswordValidator,))
    password2 = serializers.CharField(validators=(PasswordValidator,))

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Password Not Same!')
        return data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, validators=(UnicodeUsernameValidator,))
    password = serializers.CharField(validators=(PasswordValidator,))