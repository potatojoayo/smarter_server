# Generated by Django 3.2.12 on 2023-07-06 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cs', '0048_rename_status_changerequest_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='changerequestdetail',
            name='additional_price',
            field=models.IntegerField(default=0),
        ),
    ]
