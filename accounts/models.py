from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=13,
                                    validators=(RegexValidator('09(1[0-9]|3[1-9]|2[1-9])-?[0-9]{3}-?[0-9]{4}'),),
                                    unique=True)
