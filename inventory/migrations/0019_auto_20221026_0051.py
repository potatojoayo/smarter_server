# Generated by Django 3.2.12 on 2022-10-26 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0018_auto_20221026_0047'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryreceiveddetail',
            name='price_vendor',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='inventoryreceiveddetail',
            name='price_vendor_total',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='inventoryreceiveddetail',
            name='quantity_ordered',
            field=models.IntegerField(null=True),
        ),
    ]
