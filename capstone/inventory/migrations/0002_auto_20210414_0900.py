# Generated by Django 3.1.7 on 2021-04-14 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
    ]
