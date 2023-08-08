from django.db import models


class ClassPaymentRequest(models.Model):
    method = models.CharField(max_length=10)
    amount = models.IntegerField(null=True)
    orderId = models.CharField(max_length=64, unique=True)
    orderName = models.CharField(max_length=100)
    customerName = models.CharField(max_length=30)
    requestedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}. {}, {}, {}'.format(self.id, self.method, self.amount, self.orderId)
