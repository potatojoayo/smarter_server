import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from base_classes import CountableConnectionBase
from inventory.models import InventoryReceivedDetail


class InventoryReceivedDetailNode(DjangoObjectType):
    class Meta:
        model = InventoryReceivedDetail
        interfaces = (relay.Node, )
        filter_fields = {}
        connection_class = CountableConnectionBase


    detail_id = graphene.Int()


    @staticmethod
    def resolve_detail_id(root, _):
        return root.id
