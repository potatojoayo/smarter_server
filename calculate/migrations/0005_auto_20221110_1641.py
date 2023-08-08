# Generated by Django 3.2.12 on 2022-11-10 07:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('calculate', '0004_auto_20221110_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='agencycalculate',
            name='date_from',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agencycalculate',
            name='date_to',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subcontractorcalculate',
            name='date_from',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subcontractorcalculate',
            name='date_to',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='agencycalculate',
            name='agency_total_sell',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='agencycalculate',
            name='price_platform',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='agencycalculate',
            name='price_profit',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='subcontractorcalculate',
            name='total_price_work',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='subcontractorcalculate',
            name='total_price_work_labor',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='subcontractorcalculate',
            name='work_amount',
            field=models.IntegerField(default=0),
        ),
    ]
