# Generated by Django 4.2.3 on 2023-07-11 15:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0014_account_plan'),
    ]

    operations = [
        migrations.AddField(
            model_name='account_plan',
            name='changed',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='account_plan',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2023, 7, 11, 15, 2, 11, 653098, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
