from django.core.files import File
from django.db import transaction

from product.models import ProductMaster

def run():
    with transaction.atomic():
        product_masters = ProductMaster.objects.filter(description_image='')
        for product_master in product_masters:
            product_master.description_image.save('info-image.jpg', File(open('files/info-image.jpg', 'rb')))
            print(product_master.name)


