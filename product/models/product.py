from django.db import models


class Product(models.Model):

    class Meta:
        ordering = ('date_created', )

    product_master = models.ForeignKey('product.ProductMaster', on_delete=models.PROTECT, related_name='products')
    model_number = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=10)
    size = models.CharField(max_length=50)

    # 추가금
    price_additional = models.IntegerField(default=0)

    # 상태
    state = models.CharField(max_length=10)
    lack_inventory = models.BooleanField(default=False)
    # 재고관리
    inventory_quantity = models.IntegerField()
    expected_inventory_quantity = models.IntegerField()
    goal_inventory_quantity = models.IntegerField(null=True)
    threshold_inventory_quantity = models.IntegerField(null=True)

    # 날짜
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # 삭제
    is_deleted = models.BooleanField(default=False)

    @property
    def pseudo_inventory_quantity(self):
        return self.inventory_quantity + self.expected_inventory_quantity

    def __str__(self):
        return self.name

