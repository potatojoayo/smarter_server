# Generated by Django 3.2.12 on 2023-06-30 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_auto_20230403_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='refund_account_owner',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]