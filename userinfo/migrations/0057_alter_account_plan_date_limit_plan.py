# Generated by Django 4.2.2 on 2023-08-14 22:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0056_alter_account_plan_date_limit_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account_plan',
            name='date_limit_plan',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 12, 22, 4, 4, 91243, tzinfo=datetime.timezone.utc)),
        ),
    ]
