# Generated by Django 3.2.12 on 2022-11-02 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0022_remove_notice_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='contents',
            field=models.TextField(),
        ),
    ]
