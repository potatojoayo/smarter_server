# Generated by Django 3.2.12 on 2022-10-25 04:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20221020_0420'),
        ('inventory', '0005_auto_20221024_1531'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryOrderMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=10)),
                ('memo', models.TextField(blank=True, null=True)),
                ('price_total', models.IntegerField()),
                ('price_received', models.IntegerField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_scheduled_receiving', models.DateTimeField(null=True)),
                ('date_close', models.DateTimeField(null=True)),
                ('is_activate', models.BooleanField(default=True)),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.supplier')),
            ],
        ),
        migrations.RemoveField(
            model_name='inventoryorder',
            name='state',
        ),
        migrations.RemoveField(
            model_name='inventoryorder',
            name='supplier',
        ),
        migrations.RenameModel(
            old_name='InventoryOrderedProduct',
            new_name='InventoryOrderDetail',
        ),
        migrations.DeleteModel(
            name='InventoryOrderState',
        ),
        migrations.AlterField(
            model_name='changehistory',
            name='inventory_order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='inventory.inventoryordermaster'),
        ),
        migrations.AlterField(
            model_name='inventoryorderdetail',
            name='inventory_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='inventory.inventoryordermaster'),
        ),
        migrations.DeleteModel(
            name='InventoryOrder',
        ),
    ]
