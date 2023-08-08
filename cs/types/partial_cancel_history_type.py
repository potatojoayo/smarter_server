import graphene
from graphene_django import DjangoObjectType
from ..models import CsPartialCancelHistory


class PartialCancelHistoryType(DjangoObjectType):
    class Meta:
        model = CsPartialCancelHistory

    order_master_id = graphene.Int()

    @staticmethod
    def resolve_order_master_id(root: CsPartialCancelHistory, _):
        return root.order_master_id

    cs_request_id = graphene.Int()

    @staticmethod
    def resolve_cs_request_id(root: CsPartialCancelHistory, _):
        return root.cs_request_id
