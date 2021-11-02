from django.db import models
from django.contrib.auth import get_user_model


class Token(models.Model):
    key = models.CharField(max_length=100)
    user_agent = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    last_update = models.DateTimeField(auto_now=True, null=True)
    user = models.ForeignKey(get_user_model(),
                             related_name='tokens',
                             on_delete=models.CASCADE)
