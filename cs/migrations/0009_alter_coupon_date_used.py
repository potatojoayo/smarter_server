# Generated by Django 3.2.12 on 2023-06-23 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cs', '0008_auto_20230623_1527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='date_used',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
