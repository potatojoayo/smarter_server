# Generated by Django 3.2.12 on 2022-10-28 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0034_rename_date_received_inventoryreceivedmaster_date_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryreceivedmaster',
            name='receive_number',
            field=models.CharField(default=2, max_length=25, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='inventoryordermaster',
            name='inventory_order_number',
            field=models.CharField(max_length=25, unique=True),
        ),
    ]
