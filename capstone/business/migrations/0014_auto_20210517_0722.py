# Generated by Django 3.1.7 on 2021-05-17 07:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0013_auto_20210508_1135'),
    ]

    operations = [
        migrations.RenameField(
            model_name='business',
            old_name='zip_code',
            new_name='country_code',
        ),
    ]
