# Generated by Django 4.2.3 on 2023-07-11 14:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userinfo', '0013_alter_user_info_biography'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account_plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.CharField(choices=[('trial_period', 'trial period'), ('signature', 'signature'), ('free', 'free')], default='trial period', max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
