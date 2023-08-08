import graphene
from graphene import relay


class GymsStatisticsType(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node,)

    agency_name = graphene.String()
    gym_name = graphene.String()
    without_bank_payment = graphene.Int()
    card_payment = graphene.Int()
    bank_payment = graphene.Int()
    smarter_money_amount = graphene.Int()
    total_payment = graphene.Int()
    refund_amount = graphene.Int()
    total_amount = graphene.Int()






