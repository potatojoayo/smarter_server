# Generated by Django 3.2.12 on 2022-11-30 05:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gym_student', '0002_auto_20221129_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='parent',
            name='supporter_name',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='auditiondetail',
            name='did_pass',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='auditionmaster',
            name='state',
            field=models.CharField(default='진행중', max_length=15),
        ),
        migrations.AlterField(
            model_name='parent',
            name='supporter_phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='parent',
            name='supporter_relationship',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='supporter_parents', to='gym_student.relationship'),
        ),
    ]
