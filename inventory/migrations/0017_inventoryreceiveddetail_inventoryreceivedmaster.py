# Generated by Django 3.2.12 on 2022-10-25 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0016_auto_20221025_1142'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryReceivedMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiving_number', models.CharField(max_length=20, null=True)),
                ('quantity_received_total', models.IntegerField(null=True)),
                ('quantity_not_received_total', models.IntegerField(null=True)),
                ('received_price_total', models.IntegerField(null=True)),
                ('state', models.CharField(max_length=20, null=True)),
                ('date_receiving', models.DateTimeField(auto_now_add=True)),
                ('date_ordered', models.DateTimeField(null=True)),
                ('inventory_order_master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_master', to='inventory.inventoryordermaster')),
            ],
        ),
        migrations.CreateModel(
            name='InventoryReceivedDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_received', models.IntegerField(blank=True, null=True)),
                ('quantity_not_received', models.IntegerField(blank=True, null=True)),
                ('reason_not_received', models.CharField(max_length=50, null=True)),
                ('received_price', models.IntegerField(null=True)),
                ('inventory_order_detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_detail', to='inventory.inventoryorderdetail')),
            ],
        ),
    ]
