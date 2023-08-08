import graphene
from graphene_django import DjangoObjectType

from common.models import Address


class AddressType(DjangoObjectType):

    class Meta:
        model = Address

    is_default = graphene.Boolean()

    @staticmethod
    def resolve_is_default(root, __):
        return root.default
