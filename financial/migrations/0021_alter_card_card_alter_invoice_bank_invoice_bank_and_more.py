# Generated by Django 4.2.4 on 2023-10-10 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0020_alter_table_invoices_payment_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='card',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='invoice_bank',
            name='invoice_bank',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='invoice_category',
            name='invoice_category',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='payee',
            name='payee',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
    ]
