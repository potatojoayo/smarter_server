from django.db import models

from class_payment.models import ClassCardSuccess, ClassTransferSuccess, ClassEasyPaySuccess


class ClassPaymentSuccess(models.Model):
    paymentKey = models.CharField(max_length=64, null=True)
    orderId = models.CharField(max_length=64, null=True)
    amount = models.IntegerField(default=0, null=True)
    mId = models.CharField(max_length=20, null=True)
    version = models.CharField(max_length=20, null=True)
    status = models.CharField(max_length=10, null=True)
    requestedAt = models.DateTimeField(null=True)
    approvedAt = models.DateTimeField(null=True)
    card = models.ForeignKey(ClassCardSuccess, on_delete=models.CASCADE, null=True, related_name="class_payment_success")
    transfer = models.ForeignKey(ClassTransferSuccess, on_delete=models.CASCADE, null=True, related_name="class_payment_success")
    easyPay = models.ForeignKey(ClassEasyPaySuccess, on_delete=models.CASCADE, null=True, related_name="class_payment_success")
    country = models.CharField(max_length=20, null=True)
    currency = models.CharField(max_length=10, null=True)
    totalAmount = models.IntegerField(null=True)
    balanceAmount = models.IntegerField(null=True)
    suppliedAmount = models.IntegerField(null=True)
    vat = models.IntegerField(null=True)
    texFreeAmount = models.IntegerField(null=True)
    method = models.CharField(max_length=20, null=True)

    def __str__(self):
        return '{}. {}, {}, {}, {}, {}, {}'.format(self.id, self.paymentKey, self.orderId, self.amount, self.approvedAt,
                                                   self.status, self.method)
