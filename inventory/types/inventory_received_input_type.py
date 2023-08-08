import graphene


class InventoryReceivedInputType(graphene.InputObjectType):
    quantity_received = graphene.Int()
    quantity_not_received = graphene.Int()
    inventory_order_detail_id = graphene.Int()
    reason = graphene.String()


    
