from django.db import models

from inventory.models.inventory_order_master import InventoryOrderMaster
from order.models import OrderDetail
from product.models.product import Product
from product.models.product_master import ProductMaster


class ChangeHistory(models.Model):

    class Meta:
        ordering = ('-date_created',)

    order_detail = models.ForeignKey(OrderDetail, on_delete=models.CASCADE, null=True, blank=True)
    inventory_order = models.ForeignKey(InventoryOrderMaster, on_delete=models.PROTECT, null=True, blank=True)
    product_master = models.ForeignKey(ProductMaster, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    # DATE
    date_created = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=100, null=True)
    # QUANTITY
    quantity_before = models.IntegerField()
    quantity_changed = models.IntegerField()
    quantity_after = models.IntegerField()

