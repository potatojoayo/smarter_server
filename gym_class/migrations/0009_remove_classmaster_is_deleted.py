# Generated by Django 3.2.12 on 2022-12-01 11:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gym_class', '0008_auto_20221201_1946'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classmaster',
            name='is_deleted',
        ),
    ]