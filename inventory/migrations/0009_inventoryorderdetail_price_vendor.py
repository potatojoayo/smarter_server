# Generated by Django 3.2.12 on 2022-10-25 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_alter_inventoryorderdetail_price_vendor_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryorderdetail',
            name='price_vendor',
            field=models.IntegerField(null=True),
        ),
    ]