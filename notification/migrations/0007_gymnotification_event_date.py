# Generated by Django 3.2.12 on 2023-03-23 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0006_auto_20230216_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='gymnotification',
            name='event_date',
            field=models.DateField(null=True),
        ),
    ]
