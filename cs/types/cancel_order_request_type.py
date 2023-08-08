import graphene
from graphene_django import DjangoObjectType

from cs.models import CancelOrderRequest


class CancelOrderRequestType(DjangoObjectType):
    class Meta:
        model = CancelOrderRequest

    cs_request_id = graphene.Int()

    @staticmethod
    def resolve_cs_request_id(root: CancelOrderRequest, _):
        return root.cs_request_id

    order_master_id = graphene.Int()

    @staticmethod
    def resolve_order_master_id(root: CancelOrderRequest, _):
        return root.order_master_id
