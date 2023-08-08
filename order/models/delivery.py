from django.db import models

from common.models import DeliveryAgency


class Delivery(models.Model):
    delivery_agency = models.ForeignKey(DeliveryAgency, on_delete=models.PROTECT)
    tracking_number = models.CharField(max_length=100)
    photo = models.ImageField(null=True, blank=True)

