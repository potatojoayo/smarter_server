# Generated by Django 3.2.12 on 2023-02-01 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0079_auto_20230201_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermaster',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
