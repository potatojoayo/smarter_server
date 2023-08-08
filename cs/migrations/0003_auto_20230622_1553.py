# Generated by Django 3.2.12 on 2023-06-22 06:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cs', '0002_auto_20230622_1446'),
    ]

    operations = [
        migrations.CreateModel(
            name='CsRequestContents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('cs_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reqeust_contents', to='cs.csrequest')),
            ],

        ),
        migrations.DeleteModel(
            name='CsRequestContent',
        ),
    ]
