# Generated by Django 3.2.12 on 2023-06-28 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cs', '0018_couponmaster_date_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='csrequest',
            name='is_paid',
        ),
        migrations.RemoveField(
            model_name='csrequest',
            name='is_shipped',
        ),
        migrations.RemoveField(
            model_name='csrequest',
            name='is_work_completed',
        ),
        migrations.AddField(
            model_name='csrequest',
            name='order_state',
            field=models.CharField(default='결제전', max_length=20),
            preserve_default=False,
        ),
    ]
