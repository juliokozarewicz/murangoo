# Generated by Django 4.2.2 on 2023-10-11 23:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0085_alter_account_plan_date_limit_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account_plan',
            name='date_limit_plan',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 9, 23, 50, 13, 782774, tzinfo=datetime.timezone.utc)),
        ),
    ]
