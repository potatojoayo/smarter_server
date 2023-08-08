import graphene


class InventoryOrderInputType(graphene.InputObjectType):
    inventory_detail_id = graphene.Int()
    quantity_ordered = graphene.Int()
