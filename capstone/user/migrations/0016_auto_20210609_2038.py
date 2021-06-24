# Generated by Django 3.2.3 on 2021-06-09 20:38

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_auto_20210517_0628'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='mobile_number',
            new_name='phone_number',
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(null=True, upload_to=user.models.profile_image_upload_dir),
        ),
    ]