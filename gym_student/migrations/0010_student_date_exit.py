# Generated by Django 3.2.12 on 2022-12-14 10:10


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym_student', '0009_auto_20221209_1333'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='date_exit',
            field=models.DateField(blank=True, null=True),
        ),
    ]
