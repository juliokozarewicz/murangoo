# Generated by Django 4.2.4 on 2023-10-10 15:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0080_alter_account_plan_date_limit_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account_plan',
            name='date_limit_plan',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 8, 15, 50, 45, 867886, tzinfo=datetime.timezone.utc)),
        ),
    ]
