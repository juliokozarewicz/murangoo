# Generated by Django 4.2.3 on 2023-07-12 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0018_account_plan_value_alter_account_plan_plan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account_plan',
            name='value',
        ),
    ]
