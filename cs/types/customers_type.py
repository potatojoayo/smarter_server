import graphene

from business.types import GymType


class CustomersType(graphene.ObjectType):

    customers = graphene.List(GymType)
    total_count = graphene.Int()
