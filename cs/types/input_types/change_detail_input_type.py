import graphene


class ChangeDetailInputType(graphene.InputObjectType):
    id = graphene.Int()
    changing_product_id = graphene.Int()
    changing_quantity = graphene.Int()
