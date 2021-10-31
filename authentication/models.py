from django.db import models
from django.contrib.auth import get_user_model


class Token(models.Model):
    key = models.CharField(max_length=50)
    user_agent = models.CharField(max_length=200)
    user = models.ForeignKey(get_user_model(),
                             related_name='tokens',
                             on_delete=models.CASCADE)
