from graphene_django import DjangoObjectType
from graphene import relay

from smarter_money.models import SmarterMoneyHistory


class SmarterMoneyHistoryNode(DjangoObjectType):

    class Meta:
        model = SmarterMoneyHistory
        filter_fields = {
            'wallet_id': ['exact']
        }
        interfaces = (relay.Node,)
