# Generated by Django 3.2.8 on 2021-11-02 07:50

import authentication.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_phone_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(max_length=11, unique=True, validators=[authentication.validators.IranPhoneNumberValidator]),
        ),
    ]
