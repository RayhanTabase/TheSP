# Generated by Django 3.1.7 on 2021-05-11 07:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0011_invoice_customer_contact'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoiceitem',
            old_name='item_name',
            new_name='inventory_name',
        ),
    ]
