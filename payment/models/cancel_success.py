from django.db import models

from payment.models import PaymentSuccess


class CancelSuccess(models.Model):
    paymentSuccess = models.ForeignKey(PaymentSuccess, on_delete=models.DO_NOTHING, related_name='cancels')
    cancelReason = models.CharField(max_length=50, null=True)
    canceledAt = models.DateTimeField(null=True)
    cancelAmount = models.IntegerField(null=True)
    taxFreeAmount = models.IntegerField(null=True)
    taxAmount = models.IntegerField(default=0, null=True)
    refundableAmount = models.IntegerField(null=True)
    easyPayDiscountAmount = models.IntegerField(null=True)
    transactionKey = models.CharField(max_length=64, null=True)
    taxExemptionAmount = models.IntegerField(null=True)
    receiptKey = models.CharField(max_length=64, null=True)

    def __str__(self):
        return '{}. {}, {}, {}'.format(self.id, self.cancelAmount,
                                       self.canceledAt, self.transactionKey)
