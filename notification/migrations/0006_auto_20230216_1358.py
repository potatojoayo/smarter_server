# Generated by Django 3.2.12 on 2023-02-16 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0005_gymnotificationimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='gymnotification',
            name='send_datetime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='gymnotification',
            name='send_type',
            field=models.CharField(max_length=10, null=True),
        ),
    ]