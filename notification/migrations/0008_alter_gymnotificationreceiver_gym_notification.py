# Generated by Django 3.2.12 on 2023-04-14 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0007_gymnotification_event_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gymnotificationreceiver',
            name='gym_notification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receivers', to='notification.gymnotification'),
        ),
    ]
