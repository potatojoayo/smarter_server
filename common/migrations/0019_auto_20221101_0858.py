# Generated by Django 3.2.12 on 2022-11-01 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0018_notice'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notice',
            options={'ordering': ('-date_created',)},
        ),
        migrations.AddField(
            model_name='notice',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]