# Generated by Django 3.2.12 on 2023-07-04 04:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0089_workdetail_new_draft'),
        ('cs', '0033_merge_20230704_1322'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CsOrderChangeHistory',
            new_name='CsPartialCancelHistory',
        ),
        migrations.AlterModelTable(
            name='cspartialcancelhistory',
            table='cs_partial_cancel_histories',
        ),
    ]
