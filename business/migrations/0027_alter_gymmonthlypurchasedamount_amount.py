# Generated by Django 3.2.12 on 2023-07-19 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0026_gym_total_purchased_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gymmonthlypurchasedamount',
            name='amount',
            field=models.IntegerField(default=0),
        ),
    ]