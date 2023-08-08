import graphene

from order.types.order_detail_type import OrderDetailType
from order.types.order_master_node import OrderMasterNode


class OrderDetailsWithChildrenType(graphene.ObjectType):

    order_details = graphene.List(OrderDetailType)
    added_order_masters = graphene.List(OrderMasterNode)
