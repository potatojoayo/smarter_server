import graphene


class AddInventoryOrderInputType(graphene.InputObjectType):
    product_id = graphene.Int()
    quantity_ordered = graphene.Int()
