# Generated by Django 3.2.12 on 2023-06-23 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0025_newdraft'),
    ]

    operations = [
        migrations.AddField(
            model_name='newdraft',
            name='printing',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
