# Generated by Django 4.2.2 on 2023-07-12 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0021_alter_account_plan_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account_plan',
            name='plan',
            field=models.CharField(choices=[('0', 'trial period'), ('0', 'trial period'), ('0', 'trial period')], default='trial period', max_length=50),
        ),
    ]
