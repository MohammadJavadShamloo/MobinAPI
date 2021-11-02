from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from authentication.validators import IranPhoneNumberValidator


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=11,
                                    validators=(IranPhoneNumberValidator,),
                                    unique=True)
    is_phone_confirmed = models.BooleanField(default=False)
