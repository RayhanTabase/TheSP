# Generated by Django 3.2.3 on 2021-06-05 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_auto_20210508_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='unit',
            field=models.CharField(default='other', max_length=8),
        ),
    ]