# Generated by Django 3.2.12 on 2022-11-08 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0025_faq'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='condition',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='max',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='percentage',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='threshold',
            field=models.IntegerField(null=True),
        ),
    ]
