# Generated by Django 3.1.7 on 2021-05-04 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0009_auto_20210503_0815'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='zip_code',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
