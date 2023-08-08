from graphene_django import DjangoObjectType

from cs.models import CouponUseHistory


class CouponUseHistoryType(DjangoObjectType):
    class Meta:
        model = CouponUseHistory