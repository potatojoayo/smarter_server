# Generated by Django 3.2.12 on 2022-11-13 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_user_identification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='refund_account_bank',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='refund_account_no',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]