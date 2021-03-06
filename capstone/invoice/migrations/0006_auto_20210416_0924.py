# Generated by Django 3.1.7 on 2021-04-16 09:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0005_delete_invoicelog'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceitem',
            name='serviced_item',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='invoiceitem',
            name='serviced_item_finished',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='invoiceitem',
            name='serviced_item_image_check',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='ServicedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='invoice/customer_items')),
                ('invoice_item', models.ForeignKey(limit_choices_to={'serviced_item': 'True'}, on_delete=django.db.models.deletion.CASCADE, to='invoice.invoiceitem')),
            ],
        ),
    ]
