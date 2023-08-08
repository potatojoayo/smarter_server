from graphene_django import DjangoObjectType

from common.models.membership import Membership


class MembershipType(DjangoObjectType):
    class Meta:
        model = Membership
        