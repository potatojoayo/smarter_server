# Generated by Django 3.2.12 on 2023-07-20 04:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cs', '0065_couponmasterissuehistory_date_issued'),
        ('order', '0098_merge_20230720_1306'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermaster',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='order', to='cs.coupon'),
        ),
    ]
