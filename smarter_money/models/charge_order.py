from django.db import models


class ChargeOrder(models.Model):

    class Meta:
        ordering = ('date_created',)

    order_id = models.CharField(max_length=24, primary_key=True)
    order_name = models.CharField(max_length=10)
    user = models.ForeignKey('authentication.User', on_delete=models.PROTECT, related_name='charge_requests')
    amount = models.IntegerField()
    method = models.CharField(max_length=10, null=True)
    state = models.CharField(max_length=10)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
