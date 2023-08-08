from django.db import models
from order.models import Work, OrderDetail
from product.models import Draft, NewDraft


class WorkDetail(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='work_details')
    order_detail = models.ForeignKey(OrderDetail, on_delete=models.CASCADE, related_name='work_details')
    draft = models.ForeignKey(Draft, on_delete=models.PROTECT, related_name='works', null=True)
    date_finished = models.DateTimeField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    new_draft = models.ForeignKey(NewDraft, on_delete=models.PROTECT, related_name='works', null=True)



