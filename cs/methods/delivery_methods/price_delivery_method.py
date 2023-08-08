import math

from order.models import ZipCode
from product.models import Product, ProductMaster


def price_delivery_method(cs_request, order_details=None, products_info=None):
    user = cs_request.gym.user
    gym = user.gym
    delivery_price_normals = [0]
    delivery_price_divisions = [0]
    delivery_price_individuals = [0]
    extra_delivery = ZipCode.objects.filter(zip_code=gym.zip_code).first()
    if extra_delivery:
        extra_delivery_price = extra_delivery.additional_delivery_price
    else:
        extra_delivery_price = 0
    product_masters = {}
    if order_details:
        for order_detail in order_details:
            product_master_id = str(order_detail['order_detail'].product_master.id)
            if product_master_id in product_masters:
                product_masters[product_master_id]['quantity'] += order_detail['quantity']
            else:
                product_masters[product_master_id] = {'quantity': order_detail['quantity']}
    elif products_info:
        for product_info in products_info:
            product = Product.objects.get(pk=product_info.product_id)
            product_master = product.product_master
            product_master_id = product_master.id
            if product_master_id in product_masters:
                product_masters[product_master_id]['quantity'] += product_info.quantity
            else:
                product_masters[product_master_id] = {'quantity': product_info.quantity}
    for key, value in product_masters.items():
        product_master = ProductMaster.objects.get(pk=int(key))
        delivery_type = product_master.delivery_type
        quantity = value['quantity']
        price_delivery = product_master.price_delivery
        # 도서산간 지역의 zip code를 가지고 있으면 추가 배송비 지챈
        if delivery_type == '일반배송상품':
            total_price_delivery = price_delivery + extra_delivery_price
            delivery_price_normals.append(total_price_delivery)
        elif delivery_type == '분할배송상품':
            max_quantity_per_box = product_master.max_quantity_per_box
            delivery_price_division = math.ceil(quantity / max_quantity_per_box)
            total_price_delivery = (price_delivery + extra_delivery_price) * delivery_price_division
            delivery_price_divisions.append(total_price_delivery)
        else:
            total_price_delivery = (price_delivery + extra_delivery_price) * quantity
            delivery_price_individuals.append(total_price_delivery)
    # total_delivery_price = max(delivery_price_normals) + sum(delivery_price_divisions) + sum(delivery_price_individuals)
    print(delivery_price_normals)
    print(delivery_price_divisions)
    print(delivery_price_individuals)
    return delivery_price_normals, delivery_price_divisions, delivery_price_individuals



