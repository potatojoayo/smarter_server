# Generated by Django 3.2.12 on 2023-06-23 01:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0026_newdraft_printing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newdraft',
            name='draft_image',
        ),
    ]
