# Generated by Django 4.2.2 on 2023-08-11 21:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0049_alter_account_plan_date_limit_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account_plan',
            name='date_limit_plan',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 9, 21, 13, 15, 735321, tzinfo=datetime.timezone.utc)),
        ),
    ]
