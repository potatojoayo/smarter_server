# Generated by Django 3.2.12 on 2022-11-15 05:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0016_alter_productmaster_options'),
        ('order', '0055_alter_orderdetail_work'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='draft',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='works', to='product.draft'),
        ),
    ]
