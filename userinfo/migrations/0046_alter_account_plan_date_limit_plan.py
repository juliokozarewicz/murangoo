# Generated by Django 4.2.3 on 2023-08-09 11:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0045_alter_account_plan_date_limit_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account_plan',
            name='date_limit_plan',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 7, 11, 55, 10, 468355, tzinfo=datetime.timezone.utc)),
        ),
    ]
