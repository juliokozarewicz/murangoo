# Generated by Django 4.2.2 on 2023-08-15 20:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0060_alter_account_plan_date_limit_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account_plan',
            name='date_limit_plan',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 13, 20, 1, 6, 968828, tzinfo=datetime.timezone.utc)),
        ),
    ]
