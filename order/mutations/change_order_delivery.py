import graphene
import math
from django.db import transaction

from common.models import Address
from order.models import OrderMaster, ZipCode
from product.models import ProductMaster


class ChangeOrderDelivery(graphene.Mutation):
    class Arguments:
        address_id = graphene.Int()
        order_master_id = graphene.Int()

    success = graphene.Boolean()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, address_id ,order_master_id):
        address = Address.objects.get(pk=address_id)
        order_master = OrderMaster.objects.get(pk=order_master_id)
        new_extra_delivery = ZipCode.objects.filter(zip_code=address.zip_code)
        old_extra_delivery = ZipCode.objects.filter(zip_code=order_master.zip_code)
        if new_extra_delivery.exists() == old_extra_delivery.exists():
            if new_extra_delivery.exists():
                if new_extra_delivery.first().additional_delivery_price == old_extra_delivery.first().additional_delivery_price:
                    order_master.receiver = address.receiver
                    order_master.email = address.email
                    order_master.phone = address.phone
                    order_master.zip_code = address.zip_code
                    order_master.address = address.address
                    order_master.detail_address = address.detail_address
                    order_master.save()
                    return ChangeOrderDelivery(success=True)
            else:
                order_master.receiver = address.receiver
                order_master.email = address.email
                order_master.phone = address.phone
                order_master.zip_code = address.zip_code
                order_master.address = address.address
                order_master.detail_address = address.detail_address
                order_master.save()
                return ChangeOrderDelivery(success=True)
        products = order_master.details.filter(is_deleted=False).values_list('product_master__id','quantity')
        delivery_price_normals = [0]
        delivery_price_divisions = [0]
        delivery_price_individuals = [0]
        product_masters = {}
        for product in products:
            product_master_id = str(product[0])
            if product[0] in product_masters:
                product_masters[product_master_id]['quantity'] += product[1]
            else:
                product_masters[product_master_id] = {'quantity':product[1]}
        extra_delivery = ZipCode.objects.filter(zip_code=address.zip_code)
        if extra_delivery.exists():
            extra_delivery_price = extra_delivery.first().additional_delivery_price
        else:
            extra_delivery_price = 0
        for key, value in product_masters.items():
            product_master = ProductMaster.objects.get(pk=int(key))
            delivery_type = product_master.delivery_type
            quantity = value['quantity']
            price_delivery = product_master.price_delivery
            if delivery_type == "일반배송상품":
                total_price_delivery = price_delivery + extra_delivery_price
                delivery_price_normals.append(total_price_delivery)
            elif delivery_type == "분할배송상품":
                max_quantity_per_box = product_master.max_quantity_per_box
                delivery_price_division = math.ceil(quantity/max_quantity_per_box)
                total_price_delivery = (price_delivery+extra_delivery_price) * delivery_price_division
                delivery_price_divisions.append(total_price_delivery)
            else:
                total_price_delivery = (price_delivery + extra_delivery_price) * quantity
                delivery_price_individuals.append(total_price_delivery)
        total_delivery_price = max(delivery_price_normals) + sum(delivery_price_divisions) + sum(delivery_price_individuals)
        order_master.price_delivery = total_delivery_price
        order_master.receiver = address.receiver
        order_master.email = address.email
        order_master.phone = address.phone
        order_master.zip_code = address.zip_code
        order_master.address = address.address
        order_master.detail_address = address.detail_address
        order_master.save()
        return ChangeOrderDelivery(success=True)





