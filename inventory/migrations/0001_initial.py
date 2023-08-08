
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChangeHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('quantity_before', models.IntegerField()),
                ('quantity_after', models.IntegerField()),
                ('quantity_received', models.IntegerField(blank=True, null=True)),
                ('quantity_returned', models.IntegerField(blank=True, null=True)),
                ('quantity_changed_in', models.IntegerField(blank=True, null=True)),
                ('quantity_changed_out', models.IntegerField(blank=True, null=True)),
                ('quantity_sold', models.IntegerField(blank=True, null=True)),
                ('quantity_defected', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='InventoryOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('memo', models.TextField(blank=True, null=True)),
                ('price_total', models.IntegerField()),
                ('price_received', models.IntegerField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_scheduled_receiving', models.DateTimeField(null=True)),
                ('date_close', models.DateTimeField(null=True)),
                ('is_activate', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='InventoryOrderState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('business_registration_number', models.CharField(blank=True, max_length=12, null=True)),
                ('business_registration_certificate', models.FileField(blank=True, null=True, upload_to='')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('manager', models.CharField(max_length=10)),
                ('phone', models.CharField(max_length=13)),
                ('fax', models.CharField(blank=True, max_length=13, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InventoryOrderedProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_total', models.IntegerField()),
                ('note', models.CharField(max_length=50)),
                ('quantity_ordered', models.IntegerField()),
                ('quantity_received', models.IntegerField(blank=True, null=True)),
                ('quantity_not_received', models.IntegerField(blank=True, null=True)),
                ('reason_not_received', models.CharField(max_length=50)),
                ('inventory_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='inventory.inventoryorder')),
            ],
        ),
    ]
