# Generated by Django 4.2.3 on 2023-07-12 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0019_remove_account_plan_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account_plan',
            name='plan',
            field=models.CharField(choices=[('trial_period', 'trial period'), ('1', 'signature'), ('2', 'free')], default='trial period', max_length=50),
        ),
    ]
