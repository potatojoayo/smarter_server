from django.db import models

from inventory.models.inventory_order_master import InventoryOrderMaster
from product.models.product import Product


class InventoryOrderDetail(models.Model):

    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='inventory_order')
    inventory_order_master = models.ForeignKey(InventoryOrderMaster, on_delete=models.CASCADE, related_name='details')

    price_vendor_total = models.IntegerField()
    price_vendor = models.IntegerField(null=True)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=10)
    size = models.CharField(max_length=10)
    note = models.CharField(max_length=50, null=True)

    # QUANTITY
    quantity_ordered = models.IntegerField()
    # 추가
    inventory_quantity = models.IntegerField()
    expected_inventory_quantity = models.IntegerField(null=True, blank=True)
    goal_inventory_quantity = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(null=True)
