import graphene

from order.types.ta.ta_order_master_type import TaOrderMasterType


class TaOrderMastersType(graphene.ObjectType):
    ta_order_masters = graphene.List(TaOrderMasterType)
    total_count = graphene.Int()