# Generated by Django 3.2.12 on 2022-10-24 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_rename_price_product_orderdetail_price_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='price_option',
            field=models.IntegerField(default=0),
        ),
    ]
