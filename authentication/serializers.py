from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from .models import Token
from .validators import IranPhoneNumberValidator, PasswordValidator


class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, validators=(UnicodeUsernameValidator,))
    phone_number = serializers.CharField(validators=(IranPhoneNumberValidator,))
    password1 = serializers.CharField(validators=(PasswordValidator,))
    password2 = serializers.CharField(validators=(PasswordValidator,))

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Password Not Same!')
        return data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, validators=(UnicodeUsernameValidator,))
    password = serializers.CharField(validators=(PasswordValidator,))


class SendOtpSerializer(serializers.Serializer):
    phone_number = serializers.CharField(validators=(IranPhoneNumberValidator,))


class ValidateOtpSerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=4)


class ChangePassSerializer(serializers.Serializer):
    old_pass = serializers.CharField(validators=(PasswordValidator,))
    new_password1 = serializers.CharField(validators=(PasswordValidator,))
    new_password2 = serializers.CharField(validators=(PasswordValidator,))

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError('Password Not Same!')
        return data


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key',)


class KillTokenSerializer(serializers.Serializer):
    list_of_tokens = TokenSerializer(many=True)
