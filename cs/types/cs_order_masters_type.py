import graphene

from order.types.order_master_type import OrderMasterType


class CsOrderMastersType(graphene.ObjectType):
    order_masters = graphene.List(OrderMasterType)
    total_count = graphene.Int()