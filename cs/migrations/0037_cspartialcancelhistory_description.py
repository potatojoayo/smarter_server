# Generated by Django 3.2.12 on 2023-07-04 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cs', '0036_merge_0035_auto_20230704_1533_0035_auto_20230704_1709'),
    ]

    operations = [
        migrations.AddField(
            model_name='cspartialcancelhistory',
            name='description',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
