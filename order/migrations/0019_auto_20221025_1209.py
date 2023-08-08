# Generated by Django 3.2.12 on 2022-10-25 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0004_merge_20221024_0717'),
        ('order', '0018_auto_20221025_0445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='order_detail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='works', to='order.orderdetail'),
        ),
    ]