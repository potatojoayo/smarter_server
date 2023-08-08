# Generated by Django 3.2.12 on 2022-10-20 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_draftrequest_state'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='draftrequest',
            options={'ordering': ['-date_created']},
        ),
        migrations.AlterField(
            model_name='draftrequest',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='draftrequest',
            name='date_finished',
            field=models.DateTimeField(null=True),
        ),
    ]