# Generated by Django 3.2.12 on 2022-11-13 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_alter_productmaster_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmaster',
            name='description_image',
            field=models.ImageField(null=True, upload_to='product/contents'),
        ),
    ]