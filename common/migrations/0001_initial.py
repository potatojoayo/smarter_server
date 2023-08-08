
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('receiver', models.CharField(max_length=50)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(max_length=11)),
                ('zip_code', models.CharField(blank=True, max_length=5, null=True)),
                ('address', models.CharField(max_length=100)),
                ('address_detail', models.CharField(blank=True, max_length=100, null=True)),
                ('default', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=20)),
                ('number', models.CharField(max_length=50)),
                ('installment_plan_months', models.IntegerField()),
                ('is_interest_free', models.BooleanField()),
                ('approve_no', models.CharField(max_length=20)),
                ('use_card_point', models.BooleanField()),
                ('card_type', models.CharField(max_length=10)),
                ('owner_type', models.CharField(max_length=10)),
                ('acquire_status', models.CharField(max_length=20)),
                ('receipt_url', models.URLField()),
                ('amount', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryAgency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('cargo_code', models.CharField(max_length=2)),
                ('is_default', models.BooleanField()),
                ('is_active', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('contents', models.CharField(max_length=100)),
                ('notification_type', models.CharField(default='시안요청', max_length=10)),
                ('route', models.CharField(max_length=30, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_read', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=20)),
                ('account_no', models.CharField(max_length=100)),
                ('is_default', models.BooleanField()),
                ('is_active', models.BooleanField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
