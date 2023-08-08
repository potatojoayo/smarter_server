import graphene

from common.types import AddressType


class AddressesType(graphene.ObjectType):
    addresses = graphene.List(AddressType)
    total_count = graphene.Int()