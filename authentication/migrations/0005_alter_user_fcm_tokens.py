# Generated by Django 3.2.12 on 2022-12-28 02:19

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_user_fcm_tokens'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='fcm_tokens',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255), blank=True, default=list, size=None),
        ),
    ]
