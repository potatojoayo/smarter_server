# Generated by Django 3.2.12 on 2022-10-23 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(default='시안요청', max_length=20),
        ),
    ]
