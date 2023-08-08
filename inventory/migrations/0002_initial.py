
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0001_initial'),
        ('order', '0001_initial'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryorderedproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='inventory_order', to='product.product'),
        ),
        migrations.AddField(
            model_name='inventoryorder',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.inventoryorderstate'),
        ),
        migrations.AddField(
            model_name='inventoryorder',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inventory.supplier'),
        ),
        migrations.AddField(
            model_name='changehistory',
            name='inventory_order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='inventory.inventoryorder'),
        ),
        migrations.AddField(
            model_name='changehistory',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='order.ordermaster'),
        ),
        migrations.AddField(
            model_name='changehistory',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.product'),
        ),
        migrations.AddField(
            model_name='changehistory',
            name='product_master',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.productmaster'),
        ),
    ]
