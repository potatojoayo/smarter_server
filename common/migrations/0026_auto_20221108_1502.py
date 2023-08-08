# Generated by Django 3.2.12 on 2022-11-08 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0025_faq'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ('-date_created',)},
        ),
        migrations.AlterField(
            model_name='notification',
            name='date_read',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='notification',
            name='route',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
