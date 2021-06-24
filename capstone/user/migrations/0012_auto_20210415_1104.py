# Generated by Django 3.1.7 on 2021-04-15 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_auto_20210415_1049'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='first_names',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_names',
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]