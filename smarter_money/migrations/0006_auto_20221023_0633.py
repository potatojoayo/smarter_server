# Generated by Django 3.2.12 on 2022-10-23 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smarter_money', '0005_alter_chargerequest_method'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chargerequest',
            name='request_number',
        ),
        migrations.AddField(
            model_name='chargerequest',
            name='order_id',
            field=models.CharField(default='s25123afwfa', max_length=24, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chargerequest',
            name='order_name',
            field=models.CharField(default='스마터머니 충전', max_length=10),
        ),
    ]
