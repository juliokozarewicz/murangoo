# Generated by Django 4.2.4 on 2023-12-07 12:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0108_alter_account_plan_date_limit_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account_plan',
            name='date_limit_plan',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 6, 12, 24, 34, 732438, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='privacy_policy',
            name='privacy_policy_en',
            field=models.TextField(blank=True, max_length=50000, null=True),
        ),
        migrations.AlterField(
            model_name='privacy_policy',
            name='privacy_policy_pt_br',
            field=models.TextField(blank=True, max_length=50000, null=True),
        ),
        migrations.AlterField(
            model_name='privacy_policy',
            name='service_terms_en',
            field=models.TextField(blank=True, max_length=50000, null=True),
        ),
        migrations.AlterField(
            model_name='privacy_policy',
            name='service_terms_pt_br',
            field=models.TextField(blank=True, max_length=50000, null=True),
        ),
        migrations.AlterField(
            model_name='privacy_policy',
            name='version',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
