# Generated by Django 3.2.12 on 2022-10-27 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0034_easyorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='easyorder',
            name='state',
            field=models.CharField(default='주문요청', max_length=10),
        ),
    ]
