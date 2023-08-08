from django.db import models

from business.models.business import Business


class Supplier(Business):

    manager = models.CharField(max_length=10, null=True)
    phone = models.CharField(max_length=13, null=True)
    fax = models.CharField(max_length=13, null=True, blank=True)


