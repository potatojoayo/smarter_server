# Generated by Django 3.2.12 on 2022-11-15 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0029_auto_20221115_2146'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='address_detail',
            new_name='detail_address',
        ),
    ]