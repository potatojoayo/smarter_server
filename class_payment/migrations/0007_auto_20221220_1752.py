# Generated by Django 3.2.12 on 2022-12-20 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('class_payment', '0006_classpaymentmaster_payment_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassCardSuccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=30)),
                ('number', models.CharField(max_length=20)),
                ('installmentPlanMonths', models.IntegerField()),
                ('approveNo', models.CharField(max_length=10)),
                ('cardType', models.CharField(max_length=10)),
                ('ownerType', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='ClassEasyPaySuccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider', models.CharField(max_length=20)),
                ('amount', models.IntegerField(default=0)),
                ('discountAmount', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ClassPaymentFail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20)),
                ('message', models.CharField(max_length=200)),
                ('orderId', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='ClassTossPaySuccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank', models.CharField(max_length=20)),
                ('settlementStatus', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ClassTransferSuccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank', models.CharField(max_length=20)),
                ('settlementStatus', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='classpaymentrequest',
            name='amount',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='classpaymentrequest',
            name='customerName',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='classpaymentrequest',
            name='method',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='classpaymentrequest',
            name='orderName',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='classpaymentrequest',
            name='requestedAt',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='classpaymentsuccess',
            name='amount',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='classpaymentsuccess',
            name='approvedAt',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='classpaymentsuccess',
            name='balanceAmount',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='classpaymentsuccess',
            name='country',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='classpaymentsuccess',
            name='currency',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='classpaymentsuccess',
            name='mId',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='classpaymentsuccess',
            name='method',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='classpaymentsuccess',
            name='paymentKey',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='classpaymentsuccess',
            name='requestedAt',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='classpaymentsuccess',
            name='status',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='classpaymentsuccess',
            name='suppliedAmount',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='classpaymentsuccess',
            name='texFreeAmount',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='classpaymentsuccess',
            name='totalAmount',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='classpaymentsuccess',
            name='vat',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='classpaymentsuccess',
            name='version',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='classpaymentrequest',
            name='orderId',
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='classpaymentsuccess',
            name='orderId',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.CreateModel(
            name='ClassCancelSuccess',
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
                ('paymentSuccess', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='cancels', to='class_payment.classpaymentsuccess')),
            ],
        ),
        migrations.AddField(
            model_name='classpaymentsuccess',
            name='card',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='class_payment_success', to='class_payment.classcardsuccess'),
        ),
        migrations.AddField(
            model_name='classpaymentsuccess',
            name='easyPay',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='class_payment_success', to='class_payment.classeasypaysuccess'),
        ),
        migrations.AddField(
            model_name='classpaymentsuccess',
            name='transfer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='class_payment_success', to='class_payment.classtransfersuccess'),
        ),
    ]
