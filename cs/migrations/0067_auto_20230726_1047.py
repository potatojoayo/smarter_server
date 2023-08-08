# Generated by Django 3.2.12 on 2023-07-26 01:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cs', '0066_csrequestcontents_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='changerequest',
            name='cs_request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='changes', to='cs.csrequest'),
        ),
        migrations.AlterField(
            model_name='returnrequest',
            name='cs_request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='returns', to='cs.csrequest'),
        ),
    ]