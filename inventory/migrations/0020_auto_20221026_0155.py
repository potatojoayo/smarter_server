# Generated by Django 3.2.12 on 2022-10-26 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0019_auto_20221026_0051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryordermaster',
            name='state',
            field=models.CharField(default='발주대기', max_length=10),
        ),
        migrations.AlterField(
            model_name='inventoryreceivedmaster',
            name='state',
            field=models.CharField(default='발주진행중', max_length=20),
        ),
    ]
