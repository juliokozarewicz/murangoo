# Generated by Django 4.2.4 on 2023-11-17 13:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0103_alter_account_plan_date_limit_plan_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='privacy_policy',
            name='version',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account_plan',
            name='date_limit_plan',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 15, 13, 45, 16, 878494, tzinfo=datetime.timezone.utc)),
        ),
    ]
