import graphene

from cs.types.cancel_order_request_type import CancelOrderRequestType


class CancelOrderRequestsType(graphene.ObjectType):

    cancel_order_requests = graphene.List(CancelOrderRequestType)
    total_count = graphene.Int()
