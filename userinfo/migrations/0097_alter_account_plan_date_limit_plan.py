# Generated by Django 4.2.4 on 2023-10-30 13:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0096_alter_account_plan_date_limit_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account_plan',
            name='date_limit_plan',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 28, 13, 25, 6, 749543, tzinfo=datetime.timezone.utc)),
        ),
    ]
