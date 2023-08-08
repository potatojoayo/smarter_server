import graphene
from cs.types.cs_request_type import CsRequestType


class CsRequestsType(graphene.ObjectType):
    cs_requests = graphene.List(CsRequestType)
    total_count = graphene.Int()

