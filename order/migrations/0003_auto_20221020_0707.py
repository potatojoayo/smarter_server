# Generated by Django 3.2.12 on 2022-10-20 07:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='WorkState',
        ),
        migrations.RemoveField(
            model_name='work',
            name='type',
        ),
        migrations.DeleteModel(
            name='WorkType',
        ),
    ]
