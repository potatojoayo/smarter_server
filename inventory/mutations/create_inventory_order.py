from collections import defaultdict
from datetime import datetime

import graphene

from inventory.models import InventoryOrderMaster, InventoryOrderDetail, Supplier
from product.models import Product


class CreateInventoryOrder(graphene.Mutation):
    class Arguments:
        product_ids = graphene.List(graphene.Int)
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, product_ids):
        # product에서 supplier같은것끼리 묶어주는 작업
        product_list = defaultdict(list)
        for product_id in product_ids:
            product = Product.objects.get(pk=product_id)
            product_master = product.product_master
            supplier_id = str(product_master.supplier_id)
            if supplier_id in product_list:
                product_list[supplier_id].append(product)
            else:
                product_list[supplier_id] = [product]
        for key, value in product_list.items():
            supplier = Supplier.objects.get(pk=int(key))
            products = value
            number = 'I{}'.format(datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3])
            inventory_order_master = InventoryOrderMaster.objects.create(inventory_order_number=number, supplier=supplier, state="발주대기")
            price_totals = []
            for product in products:
                product_master = product.product_master
                price_vendor = product_master.price_vendor
                quantity_ordered = product.goal_inventory_quantity - product.inventory_quantity - product.expected_inventory_quantity
                # 현재 수량이 목포수량보다 많을 경우
                if quantity_ordered < 0:
                    quantity_ordered = 0
                price_vendor_total = price_vendor * quantity_ordered
                InventoryOrderDetail.objects.create(product=product,
                                                    inventory_order_master=inventory_order_master,
                                                    inventory_quantity=product.inventory_quantity,
                                                    expected_inventory_quantity=product.expected_inventory_quantity,
                                                    goal_inventory_quantity=product.goal_inventory_quantity,
                                                    price_vendor=price_vendor,
                                                    price_vendor_total=price_vendor_total,
                                                    name=product.name,
                                                    color=product.color,
                                                    size=product.size,
                                                    quantity_ordered=quantity_ordered)

                price_totals.append(price_vendor_total)
            inventory_order_master.save()
        return CreateInventoryOrder(success=True)

