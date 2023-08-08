import graphene


class InventoryOrderMasterInputType(graphene.InputObjectType):
    supplier_id = graphene.Int()

    id = graphene.Int()
    state = graphene.String()
    memo = graphene.String()

    price_total = graphene.Int()
    date_scheduled_receiving = graphene.DateTime()

    is_activate = graphene.Boolean()

