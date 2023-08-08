from django.db import models


class BankAccount(models.Model):

    class Meta:
        ordering = ('id',)

    bank_name = models.CharField(max_length=20)
    account_no = models.CharField(max_length=100)
    owner_name = models.CharField(max_length=10)
    is_default = models.BooleanField()
    is_active = models.BooleanField()

    def __str__(self):
        return self.bank_name +" - " + self.account_no