# Generated by Django 3.2.12 on 2022-12-09 04:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gym_student', '0008_student_is_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='auditionmaster',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='parent',
            name='relationship',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='parent', to='gym_student.relationship'),
        ),
    ]
