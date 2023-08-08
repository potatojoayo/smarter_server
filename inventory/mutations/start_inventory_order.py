import graphene

from inventory.models import InventoryOrderMaster, InventoryOrderDetail


class StartInventoryOrder(graphene.Mutation):
    class Arguments:
        inventory_order_master_id = graphene.Int()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, inventory_order_master_id):
        InventoryOrderMaster.objects.filter(pk=inventory_order_master_id).update(state='발주진행중')
        inventory_order_master = InventoryOrderMaster.objects.get(pk=inventory_order_master_id)
        inventory_order_details = InventoryOrderDetail.objects.filter(inventory_order_master=
                                                                       inventory_order_master)
        for inventory_order_detail in inventory_order_details:
            quantity_ordered = inventory_order_detail.quantity_ordered
            product = inventory_order_detail.product
            product.expected_inventory_quantity += quantity_ordered
            product.save()
        return StartInventoryOrder(success=True)




