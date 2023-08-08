import graphene


class InventoryOrderDetailInputType(graphene.InputObjectType):
    product_id = graphene.Int()

    id = graphene.Int()

    price_vendor = graphene.Int()
    price_total = graphene.Int()
    note = graphene.String()

    #발주수량
    quantity_ordered = graphene.Int()
    #입고예정수량
    quantity_received = graphene.Int()

    date_scheduled_receiving = graphene.DateTime()
    reason_not_received = graphene.String()
