# Generated by Django 5.0.1 on 2024-02-06 12:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0113_alter_account_plan_date_limit_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account_plan',
            name='date_limit_plan',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 6, 12, 29, 5, 171538, tzinfo=datetime.timezone.utc)),
        ),
    ]
