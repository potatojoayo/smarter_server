# Generated by Django 3.2.12 on 2022-12-07 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0042_supplier_memo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryorderdetail',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
