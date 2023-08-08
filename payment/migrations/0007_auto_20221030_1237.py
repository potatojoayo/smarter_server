# Generated by Django 3.2.12 on 2022-10-30 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0006_rename_payby_paymentrequest_method'),
    ]

    operations = [
        migrations.CreateModel(
            name='EasyPaySuccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider', models.CharField(max_length=20)),
                ('amount', models.IntegerField(default=0)),
                ('discountAmount', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CancelSuccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cancelReason', models.CharField(max_length=50, null=True)),
                ('canceledAt', models.DateTimeField(null=True)),
                ('cancelAmount', models.IntegerField(null=True)),
                ('taxFreeAmount', models.IntegerField(null=True)),
                ('taxAmount', models.IntegerField(default=0, null=True)),
                ('refundableAmount', models.IntegerField(null=True)),
                ('easyPayDiscountAmount', models.IntegerField(null=True)),
                ('transactionKey', models.CharField(max_length=64, null=True)),
                ('taxExemptionAmount', models.IntegerField(null=True)),
                ('paymentSuccess', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='cancels', to='payment.paymentsuccess')),
            ],
        ),
        migrations.AddField(
            model_name='paymentsuccess',
            name='easyPay',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment_success', to='payment.easypaysuccess'),
        ),
    ]
