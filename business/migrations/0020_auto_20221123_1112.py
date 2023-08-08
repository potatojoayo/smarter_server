# Generated by Django 3.2.12 on 2022-11-23 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0019_gym_membership'),
    ]

    operations = [
        migrations.AddField(
            model_name='agency',
            name='memo',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='gym',
            name='memo',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='subcontractor',
            name='memo',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vendor',
            name='memo',
            field=models.TextField(blank=True, null=True),
        ),
    ]
