# Generated by Django 3.2.12 on 2022-10-29 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0010_auto_20221029_1146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliveryagency',
            name='cargo_code',
        ),
    ]