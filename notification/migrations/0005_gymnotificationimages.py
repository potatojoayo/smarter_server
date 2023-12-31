# Generated by Django 3.2.12 on 2022-12-20 03:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0004_merge_20221220_1247'),
    ]

    operations = [
        migrations.CreateModel(
            name='GymNotificationImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default=None, upload_to='')),
                ('gym_notification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='notification.gymnotification')),
            ],
        ),
    ]
