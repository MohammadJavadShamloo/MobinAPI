from django.core.validators import RegexValidator


class IranPhoneNumberValidator(RegexValidator):
    regex = r'09((1[0-9])|(3[1-9])|(2[1-9]))[0-9]{3}[0-9]{4}'


class PasswordValidator(RegexValidator):
    regex = r'[a-zA-Z0-9@#$%\^\&\*]{8,}'
