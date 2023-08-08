# Generated by Django 3.2.12 on 2022-10-26 08:18

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20221020_0420'),
        ('order', '0024_auto_20221025_1423'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderdetail',
            options={'ordering': ['-order_master__date_created']},
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='delivery',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='order_details', to='order.delivery'),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='draft',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='product.draft'),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='product_master',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.productmaster'),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='student_names',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=10), default=list, size=None),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='user_request',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
