import graphene
from graphene_django import DjangoObjectType
from graphene import relay
from base_classes import CountableConnectionBase

from common.models import Faq 


class FaqNode(DjangoObjectType):
    class Meta:
        model = Faq 
        interfaces = (relay.Node,)
        filter_fields = {
            'date_created': ['lte', 'gte'],
            'is_active': ['exact'],
        }
        connection_class = CountableConnectionBase

    faq_id = graphene.Int()

    @staticmethod
    def resolve_faq_id(root, _):
        return root.id