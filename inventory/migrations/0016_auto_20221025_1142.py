# Generated by Django 3.2.12 on 2022-10-25 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0015_auto_20221025_0752'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventoryorderdetail',
            name='quantity_not_received',
        ),
        migrations.RemoveField(
            model_name='inventoryorderdetail',
            name='reason_not_received',
        ),
        migrations.AddField(
            model_name='inventoryordermaster',
            name='inventory_order_number',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
