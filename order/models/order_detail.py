from django.contrib.postgres.fields import ArrayField
from django.db import models

from product.models import Draft, NewDraft
from product.models.product_master import ProductMaster
from order.models.work import Work
from .delivery import Delivery
from .order_master import OrderMaster
from product.models.product import Product


class OrderDetail(models.Model):
    class Meta:
        ordering = ['-order_master__date_created']

    order_master = models.ForeignKey(OrderMaster, on_delete=models.CASCADE, related_name='details')
    work = models.ForeignKey(Work, on_delete=models.CASCADE, blank=True, related_name='details', null=True)

    order_detail_number = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=15)
    product_master = models.ForeignKey(ProductMaster, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='order')
    quantity = models.IntegerField()
    draft = models.ForeignKey(Draft, on_delete=models.PROTECT, related_name="orders", null=True, blank=True)
    user_request = models.CharField(max_length=100, null=True, blank=True)
    new_draft = models.ForeignKey(NewDraft, on_delete=models.SET_NULL, related_name="orders", null=True, blank=True)

    # 출고일 지정
    date_to_be_shipped = models.DateField(null=True)

    # 직송요청
    is_direct_delivery = models.BooleanField(default=False)


    # 가격
    price_total = models.IntegerField(default=0)
    price_products = models.IntegerField(default=0)
    price_work = models.IntegerField(default=0)
    price_work_labor = models.IntegerField(default=0)
    price_option = models.IntegerField(default=0)

    price_gym = models.IntegerField()
    price_consumer = models.IntegerField()
    price_parent = models.IntegerField()
    price_vendor = models.IntegerField()

    # 상태변환
    is_changed = models.BooleanField(default=False, blank=True)
    is_returned = models.BooleanField(default=False, blank=True)
    is_deleted = models.BooleanField(default=False, blank=True)
    # 배송
    delivery = models.ForeignKey(Delivery, on_delete=models.PROTECT, related_name='order_details', null=True,
                                 blank=True)

    student_names = ArrayField(models.CharField(max_length=100, blank=True), default=list, blank=True)

    @property
    def price_total_consumer(self):
        return self.quantity * self.price_consumer

    @property
    def price_total_parent(self):
        return self.quantity * self.price_parent

    @property
    def price_total_vendor(self):
        return self.quantity * self.price_vendor

    def __str__(self):
        return str(self.id)
