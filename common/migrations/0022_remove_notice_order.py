# Generated by Django 3.2.12 on 2022-11-01 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0021_notice_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notice',
            name='order',
        ),
    ]
