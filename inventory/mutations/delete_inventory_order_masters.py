import graphene

from inventory.models import InventoryOrderMaster


class DeleteInventoryOrderMasters(graphene.Mutation):
    class Arguments:
        delete_inventory_order_master_ids = graphene.List(graphene.Int)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, delete_inventory_order_detail_ids):
        for delete_inventory_order_detail_id in delete_inventory_order_detail_ids:
            InventoryOrderMaster.objects.filter(pk=delete_inventory_order_detail_id).delete()

        return DeleteInventoryOrderMasters(success=True)
