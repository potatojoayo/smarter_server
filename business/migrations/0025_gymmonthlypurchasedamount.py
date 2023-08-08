# Generated by Django 3.2.12 on 2023-07-19 04:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0024_tafirm'),
    ]

    operations = [
        migrations.CreateModel(
            name='GymMonthlyPurchasedAmount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('amount', models.IntegerField()),
                ('gym', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monthly_purchased_amount', to='business.gym')),
            ],
        ),
    ]
