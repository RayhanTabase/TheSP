# Generated by Django 3.1.7 on 2021-04-12 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0004_auto_20210410_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businesspermissions',
            name='allowed',
            field=models.CharField(choices=[('access_inventory', 'ACCESS INVENTORY'), ('manage_inventory', 'MANAGE INVENTORY'), ('make_sales', 'MAKE SALES'), ('manage_sales', 'MANAGE SALES'), ('access_accounts', 'ACCESS ACCOUNTS'), ('manage_accounts', 'MANAGE ACCOUNTS'), ('manage_employees', 'MANAGE EMPLOYEES')], max_length=30),
        ),
    ]
