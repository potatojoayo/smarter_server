# Generated by Django 3.2.12 on 2023-02-14 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym_student', '0016_auto_20230214_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='price_to_pay',
            field=models.IntegerField(null=True),
        ),
    ]