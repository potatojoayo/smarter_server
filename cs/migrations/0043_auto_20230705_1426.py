# Generated by Django 3.2.12 on 2023-07-05 05:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0089_workdetail_new_draft'),
        ('product', '0030_auto_20230629_1314'),
        ('cs', '0042_auto_20230705_1422'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CsRequestChangeDetail',
            new_name='ChangeRequestDetail',
        ),
        migrations.RenameModel(
            old_name='CsRequestRefund',
            new_name='ReturnRequest',
        ),
        migrations.RenameModel(
            old_name='CsRequestRefundDetail',
            new_name='ReturnRequestDetail',
        ),
        migrations.AlterModelTable(
            name='changerequestdetail',
            table='change_request_details',
        ),
        migrations.AlterModelTable(
            name='returnrequest',
            table='return_requests',
        ),
        migrations.AlterModelTable(
            name='returnrequestdetail',
            table='return_request_detail',
        ),
    ]
