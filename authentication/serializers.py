from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from .models import Token
from .validators import IranPhoneNumberValidator, PasswordValidator
from django.core.validators import MaxValueValidator, MinValueValidator


class RegistrationSerializer(serializers.Serializer):
    """
    Registration Serializer
    Fields : (username, phone_number, password1, password2)
    """
    username = serializers.CharField(max_length=150, validators=(UnicodeUsernameValidator(),))
    phone_number = serializers.CharField(validators=(IranPhoneNumberValidator(),))
    password1 = serializers.CharField(validators=(PasswordValidator(),))
    password2 = serializers.CharField(validators=(PasswordValidator(),))

    def validate(self, data):
        """
        :param data: input data's
        :return: return data if two passwords are same
        """
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Password Not Same!')
        return super(RegistrationSerializer, self).validate(data)


class LoginSerializer(serializers.Serializer):
    """
    Login Serializer
    Fields : (username, password)
    """
    username = serializers.CharField(max_length=150, validators=(UnicodeUsernameValidator(),))
    password = serializers.CharField(validators=(PasswordValidator(),))


class SendOtpSerializer(serializers.Serializer):
    """
    Send OTP Serializer
    Fields : (phone_number,)
    """
    phone_number = serializers.CharField(validators=(IranPhoneNumberValidator(),))


class ValidateOtpSerializer(serializers.Serializer):
    """
    Validate OTP Serializer
    Fields : (otp_code,)
    """
    otp_code = serializers.CharField(max_length=4)


class ChangePassSerializer(serializers.Serializer):
    """
    Change Password Serializer
    Fields : (old_pass, new_password1, new_password2,)
    """
    old_pass = serializers.CharField(validators=(PasswordValidator(),))
    new_password1 = serializers.CharField(validators=(PasswordValidator(),))
    new_password2 = serializers.CharField(validators=(PasswordValidator(),))

    def validate(self, data):
        """
        :param data: input data's
        :return: return data if two passwords are same
        """

        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError('Password Not Same!')
        return super(ChangePassSerializer, self).validate(data)


class TokenSerializer(serializers.ModelSerializer):
    """
    Token Serializer
    Fields : Key Field of Token Model
    """

    class Meta:
        model = Token
        fields = ('key',)


class KillTokenSerializer(serializers.Serializer):
    """
    Kill Token Serializer
    Fields : (list_of_tokens,)
    """
    list_of_tokens = TokenSerializer(many=True)


class ForgotPassSerializer(serializers.Serializer):
    """
    Forgot Password Serializer
    Fields : (otp_code, phone_number, new_password1, new_password2,)
    """
    otp_code = serializers.CharField(max_length=4)
    phone_number = serializers.CharField(validators=(IranPhoneNumberValidator(),))
    new_password1 = serializers.CharField(validators=(PasswordValidator(),))
    new_password2 = serializers.CharField(validators=(PasswordValidator(),))

    def validate(self, data):
        """
        :param data: input data's
        :return: return data if two passwords are same
        """
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError('Password Not Same!')
        return data


class GetTimeSerializer(serializers.Serializer):
    """
    Get Time Serializer
    Fields : (Day Of Week, Timezone, )
    """
    day_of_week = serializers.IntegerField(validators=[MaxValueValidator(7), MinValueValidator(1)])
    timezone = serializers.CharField(max_length=50)


class CodeSerializer(serializers.Serializer):
    """
    Code Serializer
    Fields : (Code, )
    """
    code = serializers.IntegerField(validators=[MaxValueValidator(9999), MinValueValidator(1000 )])
