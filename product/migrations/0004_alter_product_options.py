# Generated by Django 3.2.12 on 2022-10-26 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20221020_0420'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('-date_created',)},
        ),
    ]
