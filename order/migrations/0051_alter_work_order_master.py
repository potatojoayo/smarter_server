# Generated by Django 3.2.12 on 2022-11-21 04:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0050_alter_ordermaster_options'),

    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='order_master',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='works', to='order.ordermaster'),
        ),
    ]
