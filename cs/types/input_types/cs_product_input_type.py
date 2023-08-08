import graphene

class CsProductInputType(graphene.InputObjectType):
    product_id = graphene.Int()
    quantity = graphene.Int()
