# Generated by Django 4.2.3 on 2023-08-01 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0010_alter_table_invoices_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table_invoices',
            name='posting_type',
            field=models.CharField(choices=[('0', 'expense'), ('1', 'revenue')], max_length=50),
        ),
    ]
