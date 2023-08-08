from graphene_django import DjangoObjectType

from order.models import Claim


class ClaimType(DjangoObjectType):
    class Meta:
        model = Claim
