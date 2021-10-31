from django.core.validators import RegexValidator


class IranPhoneNumberValidator(RegexValidator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        kwargs['regex'] = '09(1[0-9]|3[1-9]|2[1-9])-?[0-9]{3}-?[0-9]{4}'


class PasswordValidator(RegexValidator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        kwargs['regex'] = '^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$'
