# Generated by Django 3.2.12 on 2022-10-31 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0036_alter_supplier_detail_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryreceiveddetail',
            name='quantity_additioanl_received',
            field=models.IntegerField(null=True),
        ),
    ]
