import graphene

from cs.types.return_types.return_type import ReturnType


class ReturnsType(graphene.ObjectType):
    return_requests = graphene.List(ReturnType)
    total_count = graphene.Int()
