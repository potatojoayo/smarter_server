# Generated by Django 3.2.12 on 2022-12-14 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0022_gym_is_deduct_enabled'),
        ('gym_class', '0023_auto_20221214_1751'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendancedetail',
            name='gym',
        ),
        migrations.AddField(
            model_name='attendancemaster',
            name='gym',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendance_masters', to='business.gym'),
        ),
    ]
