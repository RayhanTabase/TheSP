# Generated by Django 3.1.7 on 2021-05-17 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_auto_20210517_0444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(null=True, upload_to='profile_images'),
        ),
    ]
