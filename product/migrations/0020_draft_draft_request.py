# Generated by Django 3.2.12 on 2022-11-24 00:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0019_auto_20221121_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='draft',
            name='draft_request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='drafts', to='product.draftrequest'),
        ),
    ]
