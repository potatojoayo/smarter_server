# Generated by Django 3.2.12 on 2022-12-01 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym_class', '0003_classmaster_price_deduct_per_absent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classmaster',
            name='price_deduct_per_absent',
            field=models.IntegerField(),
        ),
    ]