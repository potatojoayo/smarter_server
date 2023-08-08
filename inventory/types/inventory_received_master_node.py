import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from base_classes import CountableConnectionBase
from inventory.models import InventoryReceivedMaster


class InventoryReceivedMasterNode(DjangoObjectType):
    class Meta:
        model = InventoryReceivedMaster
        interfaces = (relay.Node, )
        filter_fields = {
            'state': ['exact'],
            'date_created': ['lte', 'gte']
        }
        connection_class = CountableConnectionBase

    quantity_total_ordered = graphene.Int()
    quantity_total_received = graphene.Int()
    quantity_total_not_received = graphene.Int()
    quantity_total_additional_received = graphene.Int()
    price_total_received = graphene.Int()
    price_total_ordered = graphene.Int()
    price_total_additional_received = graphene.Int()

    @staticmethod
    def resolve_quantity_total_ordered(root, _):
        return root.quantity_total_ordered

    @staticmethod
    def resolve_quantity_total_received(root, _):
        return root.quantity_total_received

    @staticmethod
    def resolve_quantity_total_not_received(root, _):
        return root.quantity_total_not_received

    @staticmethod
    def resolve_price_total_ordered(root, _):
        return root.price_total_ordered

    @staticmethod
    def resolve_price_total_received(root, _):
        return root.price_total_received

    @staticmethod
    def resolve_price_total_additional_received(root, _):
        return root.price_total_additional_received

    @staticmethod
    def resolve_quantity_total_additional_received(root, _):
        return root.quantity_total_additional_received


