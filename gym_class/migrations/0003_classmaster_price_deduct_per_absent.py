# Generated by Django 3.2.12 on 2022-12-01 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym_class', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='classmaster',
            name='price_deduct_per_absent',
            field=models.IntegerField(null=True),
        ),
    ]
