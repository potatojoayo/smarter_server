# Generated by Django 3.2.12 on 2023-07-25 06:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cs', '0066_csrequestcontents_parent'),
        ('order', '0099_ordermaster_coupon'),
        ('smarter_money', '0015_auto_20230104_1146'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmarterPaidHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('reason', models.CharField(max_length=50)),
                ('change_request', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='smarter_paid_histories', to='cs.changerequest')),
                ('order_detail', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='smarter_paid_histories', to='order.orderdetail')),
                ('return_request', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='smarter_paid_histories', to='cs.returnrequest')),
            ],
        ),
    ]