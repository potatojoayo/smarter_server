# Generated by Django 3.2.12 on 2023-07-13 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0030_auto_20230629_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmaster',
            name='memo',
            field=models.TextField(null=True),
        ),
    ]
