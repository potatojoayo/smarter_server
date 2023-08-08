import graphene

from inventory.models import InventoryOrderDetail


class DeleteInventoryOrderDetails(graphene.Mutation):
    class Arguments:
        inventory_order_detail_ids = graphene.List(graphene.Int)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, inventory_order_detail_ids):
        for delete_inventory_order_detail_id in inventory_order_detail_ids:
            InventoryOrderDetail.objects.filter(pk=delete_inventory_order_detail_id).delete()

        return DeleteInventoryOrderDetails(success=True)
