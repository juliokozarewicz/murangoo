# Generated by Django 4.2.3 on 2023-07-24 12:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0028_account_plan_date_limit_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account_plan',
            name='date_limit_plan',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 22, 12, 5, 19, 757105, tzinfo=datetime.timezone.utc)),
        ),
    ]
