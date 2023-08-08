import math

from order.models import ZipCode


def whole_cancel_details_process(whole_cancel_details, cs_request):
    user = cs_request.gym.user
    gym = user.gym
    delivery_price_normals = [0]
    delivery_price_divisions = [0]
    delivery_price_individuals = [0]
    for whole_cancel_detail in whole_cancel_details:
        order_detail = whole_cancel_detail['order_detail']
        product_number = order_detail.quantity
        max_quantity_per_box = order_detail.product_master.max_quantity_per_box
        extra_delivery = ZipCode.objects.filter(zip_code=gym.zip_code).first()
        order_detail.cancel_state = "전체취소"
        order_detail.quantity = 0

        ## 배송비 계
        if extra_delivery:
            extra_delivery_price = extra_delivery.additional_delivery_price
            if order_detail.product.product_master.delivery_type == "일반배송상품":
                delivery_price = order_detail.product.product_master.price_delivery + extra_delivery_price
                delivery_price_normals.append(delivery_price)
            elif order_detail.product.product_master.delivery_type == "분할배송상품":
                delivery_price_division = math.ceil(product_number / max_quantity_per_box)
                delivery_price = (order_detail.product.product_master.price_delivery + extra_delivery_price) * delivery_price_division
                delivery_price_divisions.append(delivery_price)
            else:
                delivery_price = (order_detail.product.product_master.price_delivery + extra_delivery_price) * product_number
                delivery_price_individuals.append(delivery_price)
        else:
            if order_detail.product.product_master.delivery_type == "일반배송상품":
                delivery_price = order_detail.product.product_master.price_delivery
                delivery_price_normals.append(delivery_price)
            elif order_detail.product.product_master.delivery_type == "분할배송상품":
                delivery_price_division = math.ceil(product_number / max_quantity_per_box)
                delivery_price = (order_detail.product.product_master.price_delivery) * delivery_price_division
                delivery_price_divisions.append(delivery_price)
            else:
                delivery_price = (order_detail.product.product_master.price_delivery) * product_number
                delivery_price_individuals.append(delivery_price)



