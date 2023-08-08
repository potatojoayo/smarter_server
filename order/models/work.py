from django.db import models
from . import OrderMaster
from business.models.subcontractor import Subcontractor


class Work(models.Model):
    order_master = models.ForeignKey(OrderMaster, on_delete=models.CASCADE, related_name='works')
    subcontractor = models.ForeignKey(Subcontractor, on_delete=models.PROTECT, null=True, blank=True, related_name='works')
    memo_by_subcontractor = models.TextField(null=True, blank=True)
    memo_by_admin = models.TextField(null=True, blank=True)
    memo_by_pre_worker = models.TextField(null=True, blank=True)
    # DATE
    date_finished = models.DateTimeField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=15, default="작업중")

    @property
    def drafts(self):
        drafts = []
        order_details = self.details.all().order_by('id')
        for order_detail in order_details:
            if order_detail.new_draft:
                drafts.append(order_detail.new_draft)
        return list(set(drafts))

    @property
    def product_names(self):
        names = []
        for order_detail in self.details.all():
            names.append(order_detail.product.name)
        return list(set(names))

