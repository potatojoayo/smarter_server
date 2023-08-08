# Generated by Django 3.2.12 on 2023-06-19 06:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0024_draft_is_deleted'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewDraft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='member/logo')),
                ('price_work', models.IntegerField(null=True)),
                ('price_work_labor', models.IntegerField(null=True)),
                ('memo', models.CharField(max_length=1000, null=True)),
                ('font', models.CharField(blank=True, max_length=20, null=True)),
                ('thread_color', models.CharField(blank=True, max_length=20, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('draft_image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.draftimage')),
                ('draft_request', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='new_drafts', to='product.draftrequest')),
                ('sub_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='new_drafts', to='product.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='new_drafts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
