import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from base_classes import CountableConnectionBase
from order.models import Claim


class ClaimNode(DjangoObjectType):
    class Meta:
        model = Claim
        interfaces = (relay.Node,)
        filter_fields = {
            'date_created': ['lte', 'gte'],
            'user__gym__name': ['icontains'],
            'state': ['exact'],
        }
        connection_class = CountableConnectionBase

    claim_id = graphene.Int()

    @staticmethod
    def resolve_claim_id(root, _):
        return root.id
