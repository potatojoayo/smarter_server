# Generated by Django 3.2.12 on 2022-10-25 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0019_auto_20221025_1209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='work',
            name='date_started',
        ),
        migrations.RemoveField(
            model_name='work',
            name='date_updated',
        ),
    ]
