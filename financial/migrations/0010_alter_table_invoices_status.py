# Generated by Django 4.2.3 on 2023-08-01 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0009_alter_table_invoices_posting_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table_invoices',
            name='status',
            field=models.CharField(choices=[('0', 'pending'), ('1', 'paid'), ('2', 'canceled')], default='pending'),
        ),
    ]
