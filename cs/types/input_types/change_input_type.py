import graphene


class ChangeInputType(graphene.InputObjectType):
    order_detail_id=  graphene.Int()
    changing_product_id = graphene.Int()
    changing_quantity = graphene.Int()
