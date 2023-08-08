import graphene

from inventory.models import InventoryOrderMaster, InventoryOrderDetail
from product.models import Product


class AddInventoryOrderDetails(graphene.Mutation):
    class Arguments:
        inventory_order_master_id = graphene.Int()
        product_ids = graphene.List(graphene.Int)

    success = graphene.Int()

    @classmethod
    def mutate(cls, _, __, inventory_order_master_id, product_ids):
        inventory_order_master = InventoryOrderMaster.objects.get(pk=inventory_order_master_id)
        price_totals = []
        for product_id in product_ids:
            product = Product.objects.get(pk=product_id)
            product_master = product.product_master
            price_vendor = product_master.price_vendor
            try:
                quantity_ordered = product_master.goal_inventory_quantity - product.inventory_quantity - product.expected_inventory_quantity
            except:
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
        return AddInventoryOrderDetails(success=True)

