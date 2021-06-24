# Generated by Django 3.1.7 on 2021-04-16 09:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0007_log'),
        ('invoice', '0008_auto_20210416_0950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='sales_agent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_invoices', to='business.employee'),
        ),
    ]