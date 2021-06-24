# Generated by Django 3.2.3 on 2021-06-13 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0017_alter_business_country_code'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Log',
        ),
        migrations.AlterField(
            model_name='businesspermissions',
            name='allowed',
            field=models.CharField(choices=[('manage_inventory', 'MANAGE INVENTORY'), ('make_sales', 'MAKE SALES'), ('manage_sales', 'MANAGE SALES'), ('access_accounts', 'ACCESS ACCOUNTS'), ('manage_accounts', 'MANAGE ACCOUNTS'), ('manage_employees', 'MANAGE EMPLOYEES')], max_length=30),
        ),
        migrations.AlterField(
            model_name='employee',
            name='name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
