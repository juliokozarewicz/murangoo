# Generated by Django 4.2.2 on 2023-08-08 23:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0041_alter_account_plan_date_limit_plan_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account_plan',
            name='date_limit_plan',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 6, 23, 30, 7, 446864, tzinfo=datetime.timezone.utc)),
        ),
    ]
