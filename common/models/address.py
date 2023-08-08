from django.db import models


class Address(models.Model):

    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='addresses')
    name = models.CharField(max_length=50)
    receiver = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=11)
    zip_code = models.CharField(max_length=5, null=True, blank=True)
    address = models.CharField(max_length=100)
    detail_address = models.CharField(max_length=100, null=True, blank=True)
    default = models.BooleanField(default=False)
    delivery_memo = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
