from django.db import models

from .brand import Brand
from .category import Category


class ProductMaster(models.Model):

    class Meta:
        ordering = ('display_order',)

    product_number = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    sub_category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='sub_products')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products')
    state = models.CharField(max_length=10, default='숨김')

    # 진열 순서
    display_order = models.IntegerField(default=0)

    # 거래처
    supplier = models.ForeignKey('inventory.Supplier', on_delete=models.PROTECT, related_name='products')

    # 작업
    need_draft = models.BooleanField(default=False)
    default_draft = models.ForeignKey('product.Draft', on_delete=models.PROTECT, null=True, blank=True)

    # 이미지
    thumbnail = models.ImageField()
    description_image = models.ImageField(upload_to='product/contents', null=True)

    # PRICE
    price_consumer = models.IntegerField()
    price_parent = models.IntegerField()
    price_gym = models.IntegerField()
    price_vendor = models.IntegerField()

    # DELIVERY
    price_delivery = models.IntegerField()
    delivery_type = models.CharField(max_length=10)
    max_quantity_per_box = models.IntegerField(null=True, blank=True)

    # INVENTORY
    goal_inventory_quantity = models.IntegerField(null=True)
    threshold_inventory_quantity = models.IntegerField(null=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    memo = models.TextField(null=True)
    def __str__(self):
        return '{}. {}'.format(self.id, self.name)

    @property
    def colors(self):
        return list(set([product.color for product in self.products.filter(is_deleted=False, state='판매중')]))

    @property
    def sizes(self):
        size_list = []
        for product in self.products.filter(is_deleted=False, state='판매중'):
            if product.size not in size_list:
                size_list.append(product.size)
        return size_list





