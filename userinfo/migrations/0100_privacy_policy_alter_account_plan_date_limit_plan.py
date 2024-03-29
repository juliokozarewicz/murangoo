# Generated by Django 4.2.4 on 2023-11-17 13:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0099_alter_account_plan_date_limit_plan'),
    ]

    operations = [
        migrations.CreateModel(
            name='privacy_policy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('changed', models.DateTimeField(auto_now=True)),
                ('privacy_policy_en', models.CharField(blank=True, null=True)),
                ('service_terms_en', models.CharField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='account_plan',
            name='date_limit_plan',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 15, 13, 23, 23, 107266, tzinfo=datetime.timezone.utc)),
        ),
    ]
