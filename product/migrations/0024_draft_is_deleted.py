# Generated by Django 3.2.12 on 2023-04-05 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0023_auto_20230331_1002'),
    ]

    operations = [
        migrations.AddField(
            model_name='draft',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
