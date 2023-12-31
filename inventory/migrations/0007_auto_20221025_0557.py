# Generated by Django 3.2.12 on 2022-10-25 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_auto_20221025_0456'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventoryorderdetail',
            old_name='inventory_order',
            new_name='inventory_order_master',
        ),
        migrations.RemoveField(
            model_name='inventoryordermaster',
            name='price_received',
        ),
        migrations.AddField(
            model_name='inventoryorderdetail',
            name='price_vendor_total',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='inventoryorderdetail',
            name='note',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='inventoryorderdetail',
            name='reason_not_received',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
