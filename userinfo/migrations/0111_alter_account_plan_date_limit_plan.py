# Generated by Django 4.2.4 on 2023-12-11 14:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0110_alter_account_plan_date_limit_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account_plan',
            name='date_limit_plan',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 10, 14, 13, 25, 536743, tzinfo=datetime.timezone.utc)),
        ),
    ]
