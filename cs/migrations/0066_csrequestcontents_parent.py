# Generated by Django 3.2.12 on 2023-07-25 05:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cs', '0065_couponmasterissuehistory_date_issued'),
    ]

    operations = [
        migrations.AddField(
            model_name='csrequestcontents',
            name='parent',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='cs.csrequestcontents'),
        ),
    ]
