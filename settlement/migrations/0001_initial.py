
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('business', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SettlementState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='SettlementSubcontractor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_settled', models.IntegerField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_from', models.DateTimeField(null=True)),
                ('date_to', models.DateTimeField(null=True)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='settlement.settlementstate')),
                ('subcontractor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='business.subcontractor')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SettlementGym',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_sales', models.IntegerField()),
                ('amount_margin', models.IntegerField()),
                ('amount_platform_fee', models.IntegerField()),
                ('amount_settled', models.IntegerField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_from', models.DateTimeField(null=True)),
                ('date_to', models.DateTimeField(null=True)),
                ('gym', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='business.gym')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='settlement.settlementstate')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SettlementAgency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_sales', models.IntegerField()),
                ('amount_margin', models.IntegerField()),
                ('amount_platform_fee', models.IntegerField()),
                ('amount_settled', models.IntegerField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_from', models.DateTimeField(null=True)),
                ('date_to', models.DateTimeField(null=True)),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='business.agency')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='settlement.settlementstate')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
