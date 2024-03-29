# Generated by Django 4.2.4 on 2023-08-16 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0017_alter_table_invoices_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table_invoices',
            name='document_number',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='table_invoices',
            name='payee',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='table_invoices',
            name='payment_amount',
            field=models.DecimalField(decimal_places=2, max_digits=11),
        ),
    ]
