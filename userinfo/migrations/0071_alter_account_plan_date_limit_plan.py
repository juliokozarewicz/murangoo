# Generated by Django 4.2.4 on 2023-09-28 16:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0070_alter_account_plan_date_limit_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account_plan',
            name='date_limit_plan',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 27, 16, 42, 14, 245247, tzinfo=datetime.timezone.utc)),
        ),
    ]
