# Generated by Django 3.2.12 on 2022-10-24 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smarter_money', '0009_rename_chargerequest_chargeorder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smartermoneyhistory',
            name='order_number',
            field=models.CharField(max_length=25, null=True),
        ),
    ]
