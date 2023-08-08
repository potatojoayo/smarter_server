import graphene

from cs.types.cs_order_detail_type import CsOrderDetailType
from order.types.delivery_type import DeliveryType


class ReturnInfoType(graphene.ObjectType):
    order_details = graphene.List(CsOrderDetailType)
    receiver = graphene.String()
    phone = graphene.String()
    address = graphene.String()
    detail_address = graphene.String()
    zip_code = graphene.String()
