
from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('order', models.IntegerField()),
                ('logo', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('order', models.IntegerField(default=-1)),
                ('depth', models.IntegerField(default=0)),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='product.category')),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Draft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='member/logo')),
                ('price_work', models.IntegerField(null=True)),
                ('price_work_labor', models.IntegerField(null=True)),
                ('memo', models.CharField(max_length=1000, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_number', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=50)),
                ('colors', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=10), default=list, size=None)),
                ('sizes', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=10), default=list, size=None)),
                ('state', models.CharField(default='숨김', max_length=10)),
                ('need_draft', models.BooleanField(default=False)),
                ('thumbnail', models.ImageField(upload_to='product/thumbnail')),
                ('description_image', models.ImageField(upload_to='product/contents')),
                ('price_consumer', models.IntegerField()),
                ('price_parent', models.IntegerField()),
                ('price_gym', models.IntegerField()),
                ('price_vendor', models.IntegerField()),
                ('price_delivery', models.IntegerField()),
                ('delivery_type', models.CharField(max_length=10)),
                ('max_quantity_per_box', models.IntegerField(blank=True, null=True)),
                ('goal_inventory_quantity', models.IntegerField(null=True)),
                ('threshold_inventory_quantity', models.IntegerField(null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='product.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='product.category')),
                ('sub_category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sub_products', to='product.category')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='inventory.supplier')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default=None, upload_to='')),
                ('product_master', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='product.productmaster')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_number', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=50)),
                ('color', models.CharField(max_length=10)),
                ('size', models.CharField(max_length=20)),
                ('price_additional', models.IntegerField(default=0)),
                ('state', models.CharField(max_length=10)),
                ('inventory_quantity', models.IntegerField()),
                ('expected_inventory_quantity', models.IntegerField()),
                ('goal_inventory_quantity', models.IntegerField(null=True)),
                ('threshold_inventory_quantity', models.IntegerField(null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('product_master', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='product.productmaster')),
            ],
        ),
        migrations.CreateModel(
            name='DraftRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_finished', models.DateField(null=True)),
                ('draft', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='request', to='product.draft')),
                ('product_master', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_masters', to='product.productmaster')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='draft_requests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='draft',
            name='product_master',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='draft', to='product.productmaster'),
        ),
        migrations.AddField(
            model_name='draft',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='drafts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='CategoryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.category')),
            ],
        ),
    ]
