# Generated by Django 4.2.2 on 2023-07-13 19:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userinfo', '0022_alter_account_plan_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account_plan',
            name='plan',
            field=models.CharField(choices=[('0', 'trial period'), ('1', 'signature'), ('2', 'free'), ('3', 'porquinha')], default='0', max_length=50),
        ),
        migrations.CreateModel(
            name='Subscription_history',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('plan', models.CharField(choices=[('0', 'trial period'), ('1', 'signature'), ('2', 'free'), ('3', 'porquinha')], max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=100)),
                ('status', models.CharField(choices=[('renewed', 'renewed'), ('refused', 'refused')], max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
