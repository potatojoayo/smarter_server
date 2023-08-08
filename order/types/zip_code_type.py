from graphene_django import DjangoObjectType

from order.models import ZipCode


class ZipCodeType(DjangoObjectType):
    class Meta:
        model = ZipCode
