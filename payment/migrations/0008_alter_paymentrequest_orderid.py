# Generated by Django 3.2.12 on 2022-11-07 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0007_auto_20221030_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentrequest',
            name='orderId',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
