from django.db import models
from inventory.models.supplier import Supplier


class InventoryOrderMaster(models.Model):

    class Meta:
        ordering = ('-date_created',)

    inventory_order_number = models.CharField(max_length=25, unique=True)
    memo = models.TextField(null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    state = models.CharField(max_length=10, null=True)
    # PRICE

    @property
    def price_total(self):
        summation = 0
        for detail in self.details.all():
            summation += detail.price_vendor_total
        return summation

    # DATE
    date_created = models.DateTimeField(auto_now_add=True)
    date_scheduled_receiving = models.DateTimeField(null=True)
    date_close = models.DateTimeField(null=True)
    date_updated = models.DateTimeField(auto_now=True)

    is_activate = models.BooleanField(default=True)


