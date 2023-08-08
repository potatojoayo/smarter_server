from django.db import models

from product.models import Category
from product.models.draft_image import DraftImage


class NewDraft(models.Model):

    draft_request = models.ForeignKey('product.DraftRequest', on_delete=models.SET_NULL, null=True, blank=True, related_name='new_drafts')
    image = models.ImageField(upload_to='member/logo', null=True, blank=True)
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='new_drafts')
    sub_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='new_drafts', null=True)
    printing = models.CharField(max_length=20, null=True)
    price_work = models.IntegerField(null=True)
    price_work_labor = models.IntegerField(null=True)
    memo = models.CharField(max_length=1000, null=True, default='')
    font = models.CharField(max_length=20, null=True, default='')
    thread_color = models.CharField(max_length=20, null=True, default='')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)




