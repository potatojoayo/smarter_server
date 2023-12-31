# Generated by Django 3.2.12 on 2022-10-24 02:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_auto_20221024_0049'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderdetail',
            old_name='price_product',
            new_name='price_products',
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='order_master',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='details', to='order.ordermaster'),
        ),
    ]
