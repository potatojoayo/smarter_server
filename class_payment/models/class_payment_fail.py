from django.db import models


class ClassPaymentFail(models.Model):
    code = models.CharField(max_length=20)
    message = models.CharField(max_length=200)
    orderId = models.CharField(max_length=64)

    def __str__(self):
        return '{}. {}, {}, {}'.format(self.id, self.code, self.message, self.orderId)
