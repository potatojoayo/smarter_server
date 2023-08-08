# Generated by Django 3.2.12 on 2022-10-26 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0020_auto_20221026_0155'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventoryreceiveddetail',
            old_name='received_price',
            new_name='received_price_total',
        ),
        migrations.AddField(
            model_name='inventoryreceivedmaster',
            name='ordered_price_total',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='inventoryreceivedmaster',
            name='quantity_ordered_total',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='inventoryordermaster',
            name='state',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='inventoryreceivedmaster',
            name='state',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
