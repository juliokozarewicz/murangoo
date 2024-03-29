# Generated by Django 4.2.4 on 2023-11-17 13:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0102_alter_account_plan_date_limit_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account_plan',
            name='date_limit_plan',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 15, 13, 28, 20, 876266, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='privacy_policy',
            name='privacy_policy_en',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='privacy_policy',
            name='service_terms_en',
            field=models.TextField(blank=True, null=True),
        ),
    ]
