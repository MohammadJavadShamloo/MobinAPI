from django.core.validators import RegexValidator


class IranPhoneNumberValidator(RegexValidator):
    regex = '09(1[0-9]|3[1-9]|2[1-9])-?[0-9]{3}-?[0-9]{4}'
    message = 'Enter a valid number contains 11 digits'


class PasswordValidator(RegexValidator):
    regex = '^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$'
    message = 'Enter a valid password minimum 8 characters contains at least one lower and upper case' \
              ' english character and one digit and one special character (#?!@$%^&*-)'
