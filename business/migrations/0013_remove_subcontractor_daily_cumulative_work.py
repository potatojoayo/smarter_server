# Generated by Django 3.2.12 on 2022-10-31 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0012_alter_subcontractor_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subcontractor',
            name='daily_cumulative_work',
        ),
    ]