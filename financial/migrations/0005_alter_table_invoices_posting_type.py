# Generated by Django 4.2.3 on 2023-07-28 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0004_table_invoices_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table_invoices',
            name='posting_type',
            field=models.CharField(choices=[('debit', 'debit'), ('credit', 'credit')], max_length=50),
        ),
    ]
