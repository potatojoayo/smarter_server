# Generated by Django 3.2.12 on 2022-10-26 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0021_auto_20221026_0343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='changehistory',
            name='quantity_changed_in',
        ),
        migrations.RemoveField(
            model_name='changehistory',
            name='quantity_changed_out',
        ),
        migrations.RemoveField(
            model_name='changehistory',
            name='quantity_defected',
        ),
        migrations.RemoveField(
            model_name='changehistory',
            name='quantity_received',
        ),
        migrations.RemoveField(
            model_name='changehistory',
            name='quantity_returned',
        ),
        migrations.RemoveField(
            model_name='changehistory',
            name='quantity_sold',
        ),
        migrations.AddField(
            model_name='changehistory',
            name='quantity_changed',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
