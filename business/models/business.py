from django.db import models


class Business(models.Model):

    name = models.CharField(max_length=50)
    business_registration_number = models.CharField(max_length=12, null=True, blank=True)
    business_registration_certificate = models.FileField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    memo = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    detail_address = models.CharField(max_length=100, null=True, blank=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
