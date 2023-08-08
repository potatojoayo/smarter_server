# Generated by Django 3.2.12 on 2022-10-21 08:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('smarter_money', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='smartermoneyhistory',
            old_name='history_type',
            new_name='transaction_type',
        ),
        migrations.AddField(
            model_name='smartermoneyhistory',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='smartermoneyhistory',
            name='history_number',
            field=models.CharField(max_length=20),
        ),
    ]