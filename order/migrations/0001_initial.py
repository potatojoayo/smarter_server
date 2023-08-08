
from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0001_initial'),
        ('business', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EasyOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('contents', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('date_read', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_detail_number', models.CharField(default='', max_length=100)),
                ('state', models.CharField(max_length=15)),
                ('quantity', models.IntegerField()),
                ('price_total', models.IntegerField(default=0)),
                ('price_product', models.IntegerField(default=0)),
                ('price_work', models.IntegerField(default=0)),
                ('price_work_labor', models.IntegerField(default=0)),
                ('tracking_number', models.CharField(blank=True, max_length=100, null=True)),
                ('student_names', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=10), default=list, size=None)),
                ('delivery_agency', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='common.deliveryagency')),
            ],
        ),
        migrations.CreateModel(
            name='OrderMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=15)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_state_changed', models.DateTimeField(blank=True, null=True)),
                ('price_delivery', models.IntegerField(default=0)),
                ('memo_by_admin', models.TextField(blank=True, null=True)),
                ('memo_by_subcontractor', models.TextField(blank=True, null=True)),
                ('memo_by_buyer', models.TextField(blank=True, null=True)),
                ('receiver', models.CharField(max_length=50)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(max_length=11)),
                ('zip_code', models.CharField(blank=True, max_length=5, null=True)),
                ('address', models.CharField(max_length=100)),
                ('address_detail', models.CharField(blank=True, max_length=100, null=True)),
                ('gym', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order', to='business.gym')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WorkState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='WorkType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=15)),
                ('draft_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('belt_left_letter', models.CharField(blank=True, max_length=20, null=True)),
                ('belt_center_letter', models.CharField(blank=True, max_length=20, null=True)),
                ('belt_right_letter', models.CharField(blank=True, max_length=20, null=True)),
                ('date_started', models.DateTimeField(blank=True, null=True)),
                ('date_finished', models.DateTimeField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('order_detail', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='order.orderdetail')),
                ('subcontractor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='business.subcontractor')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='order.worktype')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_method', models.CharField(max_length=20)),
                ('amount', models.IntegerField()),
                ('account_from', models.CharField(blank=True, max_length=50, null=True)),
                ('account_to', models.CharField(blank=True, max_length=50, null=True)),
                ('account_transaction_seq_no', models.CharField(blank=True, max_length=10, null=True)),
                ('account_balance_after_transaction', models.IntegerField(blank=True, null=True)),
                ('account_result_code', models.CharField(blank=True, max_length=10, null=True)),
                ('account_in_print_content', models.CharField(blank=True, max_length=50, null=True)),
                ('card_company', models.CharField(max_length=20)),
                ('card_number', models.CharField(max_length=50)),
                ('card_status', models.CharField(blank=True, max_length=10, null=True)),
                ('card_transaction_key', models.CharField(blank=True, max_length=50, null=True)),
                ('card_last_transaction_key', models.CharField(blank=True, max_length=50, null=True)),
                ('card_payment_key', models.CharField(blank=True, max_length=100, null=True)),
                ('card_balance_amount', models.IntegerField(blank=True, null=True)),
                ('card_supplied_amount', models.IntegerField(blank=True, null=True)),
                ('card_vat', models.IntegerField(blank=True, null=True)),
                ('card_tax_free_amount', models.IntegerField(blank=True, null=True)),
                ('card_currency', models.CharField(blank=True, max_length=20, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('order_master', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='order.ordermaster')),
            ],
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='order_master',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='order.ordermaster'),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order', to='product.product'),
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='product_master',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.productmaster'),
        ),


        migrations.AddField(
            model_name='easyorder',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
