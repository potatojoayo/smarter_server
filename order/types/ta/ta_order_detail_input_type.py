import graphene


class TaOrderDetailInputType(graphene.InputObjectType):
    id = graphene.Int()
    price_special = graphene.Int()