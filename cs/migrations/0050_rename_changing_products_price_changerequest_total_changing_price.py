# Generated by Django 3.2.12 on 2023-07-06 03:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cs', '0049_changerequestdetail_additional_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='changerequest',
            old_name='changing_products_price',
            new_name='total_changing_price',
        ),
    ]