import graphene


class PaymentPerMonthType(graphene.ObjectType):
    month = graphene.String()
    amount = graphene.Int()
