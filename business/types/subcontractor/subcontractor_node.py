import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from base_classes import CountableConnectionBase
from business.models import Subcontractor


class SubcontractorNode(DjangoObjectType):

    class Meta:
        model = Subcontractor
        interfaces = (relay.Node, )
        filter_fields = {
            'name': ['icontains']
        }
        connection_class = CountableConnectionBase

    subcontractor_id = graphene.Int()

    @staticmethod
    def resolve_subcontractor_id(root, _):
        return root.id
