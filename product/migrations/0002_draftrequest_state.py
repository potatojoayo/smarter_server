# Generated by Django 3.2.12 on 2022-10-20 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='draftrequest',
            name='state',
            field=models.CharField(default='요청', max_length=10),
            preserve_default=False,
        ),
    ]