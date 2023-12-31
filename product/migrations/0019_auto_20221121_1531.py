# Generated by Django 3.2.12 on 2022-11-21 06:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0018_alter_product_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='draftrequest',
            name='date_finished',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='draftrequest',
            name='draft',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='request', to='product.draft'),
        ),
    ]
