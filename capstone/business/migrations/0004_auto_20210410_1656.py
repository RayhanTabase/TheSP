# Generated by Django 3.1.7 on 2021-04-10 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0003_auto_20210410_1544'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='title',
        ),
        migrations.CreateModel(
            name='BusinessPosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=30)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='business.business')),
            ],
            options={
                'ordering': ('business',),
            },
        ),
        migrations.CreateModel(
            name='BusinessPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allowed', models.CharField(choices=[('access_inventory', 'ACCESS INVENTORY'), ('delete_nventory', 'DELETE INVENTORY'), ('make_sales', 'MAKE SALES'), ('access_accounts', 'ACCESS ACCOUNTS')], max_length=30)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permissions', to='business.business')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.businessposition')),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='business.businessposition'),
        ),
        migrations.AddConstraint(
            model_name='businesspermissions',
            constraint=models.UniqueConstraint(fields=('business', 'position', 'allowed'), name='unique employee permissions'),
        ),
    ]
