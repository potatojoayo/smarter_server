# Generated by Django 3.2.12 on 2022-11-02 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculate', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agencycalculate',
            old_name='agency_total_amount',
            new_name='agency_total_sell',
        ),
        migrations.RemoveField(
            model_name='agencycalculate',
            name='platform_price',
        ),
        migrations.RemoveField(
            model_name='agencycalculate',
            name='profit_price',
        ),
        migrations.AddField(
            model_name='agencycalculate',
            name='price_platform',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='agencycalculate',
            name='price_profit',
            field=models.IntegerField(null=True),
        ),
    ]
