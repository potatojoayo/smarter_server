# Generated by Django 3.2.12 on 2023-02-01 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0076_alter_orderdetail_work'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='is_pick_up',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='price_delivery',
            field=models.IntegerField(default=0),
        ),
    ]
