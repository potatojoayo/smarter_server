from django.db import models


class ZipCode(models.Model):
    zip_code = models.CharField(max_length=5, null=True, blank=True)
    address = models.CharField(max_length=100)
    additional_delivery_price = models.IntegerField()
