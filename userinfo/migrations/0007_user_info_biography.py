# Generated by Django 4.2.2 on 2023-07-03 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0006_user_info_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_info',
            name='biography',
            field=models.TextField(default='', max_length=150),
        ),
    ]
