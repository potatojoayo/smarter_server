# Generated by Django 3.2.12 on 2022-10-24 07:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_remove_ordermaster_gym'),
        ('inventory', '0003_supplier_detail_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='changehistory',
            name='order',
        ),
        migrations.AddField(
            model_name='changehistory',
            name='order_detail',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='order.orderdetail'),
        ),
        migrations.AddField(
            model_name='changehistory',
            name='reason',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
