# Generated by Django 3.2.12 on 2022-10-24 02:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_rename_price_products_orderdetail_price_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderdetail',
            old_name='price_product',
            new_name='price_products',
        ),
    ]
