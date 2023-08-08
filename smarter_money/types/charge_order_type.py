from graphene_django import DjangoObjectType

from smarter_money.models import ChargeOrder


class ChargeOrderType(DjangoObjectType):

    class Meta:
        model = ChargeOrder

