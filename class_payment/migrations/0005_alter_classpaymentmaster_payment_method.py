# Generated by Django 3.2.12 on 2022-12-01 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('class_payment', '0004_auto_20221201_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classpaymentmaster',
            name='payment_method',
            field=models.CharField(default='미납', max_length=15),
        ),
    ]
