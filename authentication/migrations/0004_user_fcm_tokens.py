# Generated by Django 3.2.12 on 2022-12-28 01:16

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20221113_2224'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='fcm_tokens',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255, null=True), blank=True, default=list, size=None),
        ),
    ]
