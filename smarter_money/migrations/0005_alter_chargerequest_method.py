# Generated by Django 3.2.12 on 2022-10-23 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smarter_money', '0004_chargerequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chargerequest',
            name='method',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
