# Generated by Django 3.2.12 on 2023-01-04 02:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0022_productmaster_default_draft'),
        ('inventory', '0044_auto_20221207_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='changehistory',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product'),
        ),
    ]
