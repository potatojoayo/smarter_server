# Generated by Django 3.2.12 on 2022-11-06 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_productmaster_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='lack_inventory',
            field=models.BooleanField(default=False, null=True),
        ),
    ]