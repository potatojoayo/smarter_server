# Generated by Django 3.2.12 on 2022-12-14 08:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gym_class', '0022_auto_20221214_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancemaster',
            name='class_detail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_master', to='gym_class.classdetail'),
        ),
        migrations.AlterField(
            model_name='attendancemaster',
            name='class_master',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='attendance_master', to='gym_class.classmaster'),
        ),
    ]
