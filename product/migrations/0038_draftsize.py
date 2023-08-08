# Generated by Django 3.2.12 on 2023-07-28 05:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0037_auto_20230728_1423'),
    ]

    operations = [
        migrations.CreateModel(
            name='DraftSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('back_width', models.IntegerField(default=0)),
                ('back_height', models.IntegerField(default=0)),
                ('left_chest_width', models.IntegerField(default=0)),
                ('left_chest_height', models.IntegerField(default=0)),
                ('right_chest_width', models.IntegerField(default=0)),
                ('right_chest_height', models.IntegerField(default=0)),
                ('left_shoulder_width', models.IntegerField(default=0)),
                ('left_shoulder_height', models.IntegerField(default=0)),
                ('right_shoulder_width', models.IntegerField(default=0)),
                ('right_shoulder_height', models.IntegerField(default=0)),
                ('heap_width', models.IntegerField(default=0)),
                ('heap_height', models.IntegerField(default=0)),
                ('left_pant_middle_width', models.IntegerField(default=0)),
                ('left_pant_middle_height', models.IntegerField(default=0)),
                ('right_pant_middle_width', models.IntegerField(default=0)),
                ('right_pant_middle_height', models.IntegerField(default=0)),
                ('left_pant_low_width', models.IntegerField(default=0)),
                ('left_pant_low_height', models.IntegerField(default=0)),
                ('right_pant_low_width', models.IntegerField(default=0)),
                ('right_pant_low_height', models.IntegerField(default=0)),
                ('flag_width', models.IntegerField(default=0)),
                ('flag_height', models.IntegerField(default=0)),
                ('new_draft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sizes', to='product.newdraft')),
            ],
        ),
    ]
