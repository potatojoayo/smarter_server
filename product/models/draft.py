from django.db import models

from product.models.draft_image import DraftImage
from product.models.product_master import ProductMaster


class Draft(models.Model):

    draft_request = models.ForeignKey('product.DraftRequest', on_delete=models.SET_NULL, null=True, blank=True, related_name='drafts')
    image = models.ImageField(upload_to='member/logo', null=True, blank=True)
    draft_image = models.ForeignKey(DraftImage, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='drafts')
    product_master = models.ForeignKey(ProductMaster, on_delete=models.CASCADE, related_name='draft', null=True)
    price_work = models.IntegerField(null=True)
    price_work_labor = models.IntegerField(null=True)
    memo = models.CharField(max_length=1000, null=True)
    font = models.CharField(max_length=20, null=True, blank=True)
    thread_color = models.CharField(max_length=20, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

