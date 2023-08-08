import graphene

class ReturnDetailInputType(graphene.InputObjectType):
    id = graphene.Int()
    return_quantity = graphene.Int()