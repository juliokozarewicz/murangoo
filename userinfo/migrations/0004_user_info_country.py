# Generated by Django 4.2.2 on 2023-06-30 22:11

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0003_remove_user_info_phone_number_alter_user_info_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_info',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True),
        ),
    ]
