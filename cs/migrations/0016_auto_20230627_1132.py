# Generated by Django 3.2.12 on 2023-06-27 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cs', '0015_alter_csrequest_order_master'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csrequest',
            name='category',
            field=models.CharField(default='일반문의', max_length=15),
        ),
        migrations.AlterField(
            model_name='csrequest',
            name='cs_state',
            field=models.CharField(default='미처리', max_length=20),
        ),
        migrations.AlterField(
            model_name='csrequest',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='csrequest',
            name='is_shipped',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='csrequest',
            name='memo',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='csrequest',
            name='request_number',
            field=models.CharField(max_length=20),
        ),
    ]