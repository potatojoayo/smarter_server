import graphene
from graphene_django import DjangoObjectType

from common.models import AddressZipCode


class AddressZipCodeType(DjangoObjectType):
    class Meta:
        model = AddressZipCode

    children = graphene.List(lambda: AddressZipCodeType)

    @staticmethod
    def resolve_children(root: AddressZipCode, _):
        return root.children.all()
