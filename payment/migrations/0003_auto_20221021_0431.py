# Generated by Django 3.2.12 on 2022-10-21 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_auto_20221021_0351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentsuccess',
            name='approvedAt',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='paymentsuccess',
            name='balanceAmount',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='paymentsuccess',
            name='country',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='paymentsuccess',
            name='currency',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='paymentsuccess',
            name='mId',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='paymentsuccess',
            name='method',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='paymentsuccess',
            name='requestedAt',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='paymentsuccess',
            name='status',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='paymentsuccess',
            name='suppliedAmount',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='paymentsuccess',
            name='texFreeAmount',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='paymentsuccess',
            name='totalAmount',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='paymentsuccess',
            name='vat',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='paymentsuccess',
            name='version',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
