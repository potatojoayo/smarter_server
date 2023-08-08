# Generated by Django 3.2.12 on 2022-11-06 06:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0025_faq'),
        ('business', '0018_remove_gym_membership'),
    ]

    operations = [
        migrations.AddField(
            model_name='gym',
            name='membership',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='membership', to='common.membership'),
        ),
    ]