# Generated by Django 3.2.8 on 2021-11-09 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_token_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchPic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='architecture/%Y/%m/%d/')),
            ],
        ),
    ]
