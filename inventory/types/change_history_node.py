from graphene import relay
from graphene_django import DjangoObjectType

from base_classes import CountableConnectionBase
from inventory.models import ChangeHistory


class ChangeHistoryNode(DjangoObjectType):
    class Meta:
        model = ChangeHistory
        interfaces = (relay.Node, )
        filter_fields = {
            'product__name': ['icontains'],
            'date_created': ['lte', 'gte']
        }
        connection_class = CountableConnectionBase
