# Generated by Django 3.2.12 on 2023-07-03 08:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0089_workdetail_new_draft'),
        ('cs', '0031_auto_20230703_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='csrequestchangedetail',
            name='delivery',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='change_details', to='order.delivery'),
        ),
    ]
