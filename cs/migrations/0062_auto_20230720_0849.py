# Generated by Django 3.2.12 on 2023-07-19 23:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cs', '0061_coupon_nominee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='referral_user',
        ),
    ]