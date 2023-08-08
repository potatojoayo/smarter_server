# Generated by Django 3.2.12 on 2022-11-24 04:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0073_alter_easyorder_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='EasyOrderFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(null=True, upload_to='member/logo/request')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('easy_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='order.easyorder')),
            ],
            options={
                'ordering': ('date_created',),
            },
        ),
    ]
