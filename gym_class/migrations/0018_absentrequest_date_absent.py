# Generated by Django 3.2.12 on 2022-12-06 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym_class', '0017_remove_absentrequest_date_absent'),
    ]

    operations = [
        migrations.AddField(
            model_name='absentrequest',
            name='date_absent',
            field=models.DateField(null=True),
        ),
    ]
