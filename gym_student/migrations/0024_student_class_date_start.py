# Generated by Django 3.2.12 on 2023-04-19 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym_student', '0023_auto_20230329_1006'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='class_date_start',
            field=models.DateField(null=True),
        ),
    ]
