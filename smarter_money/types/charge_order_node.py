from graphene_django import DjangoObjectType
from graphene import relay

from base_classes import CountableConnectionBase
from smarter_money.models import ChargeOrder


class ChargeOrderNode(DjangoObjectType):

    class Meta:
        model = ChargeOrder
        filter_fields = {
            'user__name': ['icontains'],
            'user__gym__name': ['icontains'],
            'state': ['exact']
        }
        interfaces = (relay.Node,)
        connection_class = CountableConnectionBase
