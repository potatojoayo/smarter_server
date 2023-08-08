from django.db import models
from django.db.models import Q


class OrderMaster(models.Model):

    class Meta:
        ordering = ['-date_created']

    order_number = models.CharField(max_length=25, unique=True)
    user = models.ForeignKey('authentication.User', on_delete=models.PROTECT, related_name='orders')
    parent_order = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children',default=None)
    # DATE
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_state_changed = models.DateTimeField(null=True, blank=True)

    price_delivery = models.IntegerField(default=0)

    # MEMO
    memo_by_admin = models.TextField(null=True, blank=True)
    memo_by_subcontractor = models.TextField(null=True, blank=True)
    memo_by_buyer = models.TextField(null=True, blank=True)


    # 배송 정보
    is_pick_up = models.BooleanField(default=False)
    receiver = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=11)
    zip_code = models.CharField(max_length=5, null=True, blank=True)
    address = models.CharField(max_length=100)
    detail_address = models.CharField(max_length=100, null=True, blank=True)
    delivery_request = models.CharField(max_length=100, null=True)


    is_deleted = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    coupon = models.ForeignKey('cs.Coupon', on_delete=models.PROTECT, related_name="order", blank=True, null=True)
    @property
    def price_to_pay(self):
        total = 0
        for detail in self.details.filter(is_deleted=False):
            total += detail.price_total
        for child in self.children.all():
            for detail in child.details.filter(is_deleted=False):
                total += detail.price_total
        for smarter_money_history in self.smarter_money_history.filter(transaction_type='사용'):
            total -= smarter_money_history.amount
        total -= self.coupon.price if self.coupon else 0
        total += self.price_delivery
        return total

    @property
    def order_name(self):
        detail = self.details.first()
        product_name = detail.product_master.name
        product_count = self.details.count()
        description = product_name
        if product_count > 1:
            description += ' 외 {}개 상품'.format(product_count-1)
        return description

    @property
    def price_total(self):
        total = 0
        for detail in self.details.filter(is_deleted=False):
            total += detail.price_total
        for child in self.children.all():
            for detail in child.details.filter(is_deleted=False):
                total += detail.price_total
        return total

    @property
    def price_total_products(self):
        total = 0
        for detail in self.details.filter(is_deleted=False):
            total += detail.price_products
        for child in self.children.all():
            for detail in child.details.filter(is_deleted=False):
                total += detail.price_products
        return total

    @property
    def price_total_work_labor(self):
        total = 0
        for detail in self.details.filter(is_deleted=False):
            total += detail.price_work_labor
        for child in self.children.all():
            for detail in child.details.filter(is_deleted=False):
                total += detail.price_work_labor
        return total

    @property
    def price_total_work(self):
        total = 0
        for detail in self.details.filter(is_deleted=False):
            total += detail.price_work
        for child in self.children.all():
            for detail in child.details.filter(is_deleted=False):
                total += detail.price_work
        return total

    def __str__(self):
        return self.order_number

