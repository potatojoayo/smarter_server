# Generated by Django 3.2.12 on 2022-10-21 08:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20221020_0420'),
        ('order', '0003_auto_20221020_0707'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='draft',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='product.draft'),
        ),
    ]