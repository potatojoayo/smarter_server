from django.db import models


class ExtraPriceDelivery(models.Model):

    price = models.IntegerField(default=3000)
