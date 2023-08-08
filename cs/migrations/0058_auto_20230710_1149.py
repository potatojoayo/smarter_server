# Generated by Django 3.2.12 on 2023-07-10 02:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0091_auto_20230707_1146'),
        ('cs', '0057_auto_20230710_1051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='changerequestdetail',
            name='delivery',
        ),
        migrations.AddField(
            model_name='changerequestdetail',
            name='order_detail',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='change_details', to='order.orderdetail'),
        ),
    ]
