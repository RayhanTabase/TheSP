# Generated by Django 3.1.7 on 2021-04-10 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0002_auto_20210410_1525'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='business',
            options={'ordering': ['type']},
        ),
        migrations.AlterModelOptions(
            name='employee',
            options={'ordering': ['-business', '-timestamp']},
        ),
    ]