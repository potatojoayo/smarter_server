# Generated by Django 3.2.12 on 2023-07-31 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0045_alter_changehistory_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
