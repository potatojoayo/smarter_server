# Generated by Django 3.2.12 on 2023-06-23 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0027_remove_newdraft_draft_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newdraft',
            name='font',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='newdraft',
            name='memo',
            field=models.CharField(default='', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='newdraft',
            name='thread_color',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
    ]
