# Generated by Django 3.2.12 on 2023-02-17 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym_student', '0020_alter_auditionmaster_estimated_alarm_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auditionmaster',
            name='estimated_alarm_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
