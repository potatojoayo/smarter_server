import graphene


class ChargeSmarterMoneyInputType(graphene.InputObjectType):
    order_id = graphene.String()
    user_id = graphene.Int()
