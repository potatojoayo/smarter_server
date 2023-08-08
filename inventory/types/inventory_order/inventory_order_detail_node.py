import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from inventory.models import InventoryOrderDetail


class InventoryOrderDetailNode(DjangoObjectType):
    class Meta:
        model = InventoryOrderDetail
        interfaces = (relay.Node, )
        filter_fields= {}

    detail_id = graphene.Int()

    @staticmethod
    def resolve_detail_id(root, _):
        return root.id
