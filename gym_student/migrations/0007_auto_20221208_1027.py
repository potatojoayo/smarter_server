# Generated by Django 3.2.12 on 2022-12-08 01:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gym_student', '0006_auto_20221202_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parent',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='parent', to=settings.AUTH_USER_MODEL),
        ),
    ]
