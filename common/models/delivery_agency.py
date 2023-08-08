from django.db import models


class DeliveryAgency(models.Model):
    name = models.CharField(max_length=20)
    is_default = models.BooleanField(null=True)
    is_active = models.BooleanField(null=True)

    def __str__(self):
        return self.name
