import graphene
class CalculatePriceType(graphene.ObjectType):
    total_products_price = graphene.Int()
    delivery_price = graphene.Int()
    total_refund_price = graphene.Int()
