import graphene

from inventory.models import InventoryOrderMaster, InventoryOrderDetail


class UpdateInventoryOrder(graphene.Mutation):
    class Arguments:
        inventory_order_master_id = graphene.Int()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, inventory_order_master_id):
        inventory_order_master = InventoryOrderMaster.objects.get(pk=inventory_order_master_id)
        inventory_order_details = InventoryOrderDetail.objects.filter(inventory_order_master
                                                                      =inventory_order_master)
        for inventory_order_detail in inventory_order_details:
            product = inventory_order_detail.product
            product_master = product.product_master
            inventory_order_detail.name = product.name
            inventory_order_detail.color = product.color
            inventory_order_detail.size = product.size
            inventory_order_detail.inventory_quantity = product.inventory_quantity
            inventory_order_detail.expected_inventory_quantity = product.expected_inventory_quantity
            inventory_order_detail.goal_inventory_quantity = product.goal_inventory_quantity
            inventory_order_detail.quantity_ordered = inventory_order_detail.goal_inventory_quantity-inventory_order_detail.expected_inventory_quantity-inventory_order_detail.inventory_quantity
            inventory_order_detail.price_vendor = product_master.price_vendor
            inventory_order_detail.price_vendor_total = inventory_order_detail.price_vendor * inventory_order_detail.quantity_ordered
            inventory_order_detail.date = inventory_order_master.date_created
            inventory_order_detail.save()
        inventory_order_master.save()
        return UpdateInventoryOrder(success=True)


