from django.db import models


class ClassTransferSuccess(models.Model):
    bank = models.CharField(max_length=20)
    settlementStatus = models.CharField(max_length=20)

    def __str__(self):
        return '{}. {}, {}'.format(self.id, self.bank, self.settlementStatus)
