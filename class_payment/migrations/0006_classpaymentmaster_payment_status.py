# Generated by Django 3.2.12 on 2022-12-02 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('class_payment', '0005_alter_classpaymentmaster_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='classpaymentmaster',
            name='payment_status',
            field=models.CharField(default='미납', max_length=5),
        ),
    ]
