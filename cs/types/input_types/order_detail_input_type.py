import graphene


class OrderDetailInputType(graphene.InputObjectType):
    id = graphene.Int()
    quantity = graphene.Int()