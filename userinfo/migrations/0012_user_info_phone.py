# Generated by Django 4.2.2 on 2023-07-04 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userinfo', '0011_alter_user_info_biography'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_info',
            name='phone',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
