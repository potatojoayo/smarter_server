# Generated by Django 3.2.12 on 2022-10-29 08:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0037_alter_easyorder_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='zipcode',
            old_name='cost',
            new_name='additional_delivery_price',
        ),
    ]
