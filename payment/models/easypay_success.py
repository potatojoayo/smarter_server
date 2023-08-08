from django.db import models


class EasyPaySuccess(models.Model):
    provider = models.CharField(max_length=20)
    amount = models.IntegerField(default=0)
    discountAmount = models.IntegerField(default=0)

    def __str__(self):
        return '{}. {}, {}, {}'.format(self.id, self.provider,
                                       self.amount, self.discountAmount)
