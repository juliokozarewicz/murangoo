# Generated by Django 4.2.4 on 2023-08-17 12:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0065_alter_account_plan_date_limit_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account_plan',
            name='date_limit_plan',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 15, 12, 32, 15, 946303, tzinfo=datetime.timezone.utc)),
        ),
    ]
