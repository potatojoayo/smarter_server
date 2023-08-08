# Generated by Django 3.2.12 on 2022-11-10 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculate', '0003_subcontractorcalculate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agencycalculate',
            name='agency_total_sell',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='agencycalculate',
            name='price_platform',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='agencycalculate',
            name='price_profit',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='subcontractorcalculate',
            name='total_price_work',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='subcontractorcalculate',
            name='total_price_work_labor',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='subcontractorcalculate',
            name='work_amount',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
