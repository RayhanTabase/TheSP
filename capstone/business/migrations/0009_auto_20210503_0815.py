# Generated by Django 3.1.7 on 2021-05-03 08:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0008_auto_20210418_1427'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='business',
            options={'ordering': ['-timestamp', 'name']},
        ),
        migrations.RemoveField(
            model_name='business',
            name='type',
        ),
    ]
