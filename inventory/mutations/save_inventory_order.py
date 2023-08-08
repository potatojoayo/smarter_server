import graphene

from inventory.models import Supplier, InventoryOrderMaster, InventoryOrderDetail
from inventory.types.inventory_order.inventory_order_input_type import InventoryOrderInputType


class SaveInventoryOrder(graphene.Mutation):
    class Arguments:
        inventory_order_master_id = graphene.Int()
        date_scheduled_receiving = graphene.DateTime()
        supplier_id = graphene.Int()
        inventory_order_details = graphene.List(InventoryOrderInputType)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, inventory_order_master_id, date_scheduled_receiving=None,
               supplier_id=None, inventory_order_details=None):
        if supplier_id:
            supplier = Supplier.objects.get(pk=supplier_id)
            InventoryOrderMaster.objects.filter(pk=inventory_order_master_id).update(date_scheduled_receiving
                                                                                 =date_scheduled_receiving,
                                                                                 supplier=supplier)

        InventoryOrderMaster.objects.filter(pk=inventory_order_master_id).update(date_scheduled_receiving
                                                                                 =date_scheduled_receiving
                                                                                 )

        for inventory_order_detail in inventory_order_details:
            inventory_detail_id = inventory_order_detail["inventory_detail_id"]
            quantity_ordered = inventory_order_detail["quantity_ordered"]
            InventoryOrderDetail.objects.filter(pk=inventory_detail_id).update(quantity_ordered=quantity_ordered)
        return SaveInventoryOrder(success=True)




