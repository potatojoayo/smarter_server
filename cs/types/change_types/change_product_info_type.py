import graphene


class ChangeProductInfoType(graphene.ObjectType):
    changing_product_id = graphene.Int()
    changing_price = graphene.Int()

