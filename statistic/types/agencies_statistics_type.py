import graphene
from graphene import relay


class FirstInnerItem(graphene.ObjectType):
    without_bank_payment = graphene.Int()
    card_payment = graphene.Int()
    bank_payment = graphene.Int()
    smarter_money_amount = graphene.Int()
    total_payment = graphene.Int()
    refund_amount = graphene.Int()
    total_amount = graphene.Int()


class AgenciesStatisticsType(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)

    agency_name = graphene.String()
    value = graphene.Field(FirstInnerItem)




