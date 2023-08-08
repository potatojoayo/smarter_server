import graphene

from cs.types.change_types.change_request_type import ChangeRequestType


class ChangesType(graphene.ObjectType):
    change_requests = graphene.List(ChangeRequestType)
    total_count = graphene.Int()