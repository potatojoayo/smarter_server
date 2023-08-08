from django.db import models

from inventory.models import InventoryOrderMaster


class InventoryReceivedMaster(models.Model):
    class Meta:
        ordering = ('-id',)
    receive_number = models.CharField(max_length=25, unique=True)
    inventory_order_master = models.ForeignKey(InventoryOrderMaster, on_delete=models.CASCADE, related_name='received_master')
    state = models.CharField(max_length=20, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    @property
    def quantity_total_ordered(self):
        total = 0
        details = self.details.all()
        for detail in details:
            total += detail.quantity_ordered
        return total

    @property
    def quantity_total_received(self):
        total = 0
        details = self.details.all()
        for detail in details:
            total += detail.quantity_received
            if detail.quantity_additional_received:
                total += detail.quantity_additional_received
        return total

    @property
    def quantity_total_not_received(self):
        total = 0
        details = self.details.all()
        for detail in details:
            total += detail.quantity_not_received
        return total

    @property
    def price_total_received(self):
        total = 0
        details = self.details.all()
        for detail in details:
            total += detail.price_received
            if detail.price_additional_received:
                total += detail.price_additional_received
        return total

    @property
    def price_total_ordered(self):
        total = 0
        details = self.details.all()
        for detail in details:
            total += detail.price_ordered
        return total

    @property
    def quantity_total_additional_received(self):
        total = 0
        details = self.details.all()
        for detail in details:
            if detail.quantity_additional_received:
                total += detail.quantity_additional_received
        return total

    @property
    def price_total_additional_received(self):
        total = 0
        details = self.details.all()
        for detail in details:
            if detail.price_additional_received:
                total += detail.price_additional_received
        return total

