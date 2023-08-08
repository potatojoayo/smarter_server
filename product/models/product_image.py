from django.db import models
from product.models.product_master import ProductMaster


class ProductImage(models.Model):
    product_master = models.ForeignKey(ProductMaster, on_delete=models.CASCADE, related_name='images', default=None)
    image = models.ImageField(default=None)
    # order = models.IntegerField(default=None, null=True)
