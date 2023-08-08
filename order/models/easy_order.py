from django.db import models

from order.models.order_master import OrderMaster


class EasyOrder(models.Model):

    class Meta:
        ordering = ('-date_created', )

    user = models.ForeignKey('authentication.User', on_delete=models.PROTECT)
    contents = models.TextField(null=True, blank=True)
    state = models.CharField(max_length=10, default='주문요청')
    order = models.ForeignKey(OrderMaster, on_delete=models.CASCADE, related_name='easy_order', null=True, blank=True)
    is_visit = models.BooleanField(default=False)
    is_order_more = models.BooleanField(default=False)

    # DATE
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_completed = models.DateTimeField(null=True)
    date_read = models.DateTimeField(null=True, blank=True)

