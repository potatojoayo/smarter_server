# Generated by Django 3.2.12 on 2022-10-31 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smarter_money', '0010_alter_smartermoneyhistory_order_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chargeorder',
            options={'ordering': ('date_created',)},
        ),
    ]
