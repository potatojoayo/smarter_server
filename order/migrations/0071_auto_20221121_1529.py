# Generated by Django 3.2.12 on 2022-11-21 06:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0070_auto_20221117_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claim',
            name='order_detail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='claims', to='order.orderdetail'),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='order_master',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='order.ordermaster'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='order_master',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='order.ordermaster'),
        ),
        migrations.AlterField(
            model_name='work',
            name='order_master',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='works', to='order.ordermaster'),
        ),
    ]