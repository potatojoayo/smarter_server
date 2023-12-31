# Generated by Django 3.2.12 on 2023-07-05 07:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0089_workdetail_new_draft'),
        ('cs', '0046_rename_status_returnrequest_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='returnrequestdetail',
            name='cs_request_refund',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='return_details', to='cs.returnrequest'),
        ),
        migrations.AlterField(
            model_name='returnrequestdetail',
            name='order_detail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='return_details', to='order.orderdetail'),
        ),
    ]
