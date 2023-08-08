import graphene
from graphene_django import DjangoObjectType
from graphene import relay
from base_classes import CountableConnectionBase

from common.models import Notice 


class NoticeNode(DjangoObjectType):
    class Meta:
        model = Notice 
        interfaces = (relay.Node,)
        filter_fields = {
            'date_created': ['lte', 'gte'],
            'is_active': ['exact'],
        }
        connection_class = CountableConnectionBase

    notice_id = graphene.Int()

    @staticmethod
    def resolve_notice_id(root, _):
        return root.id