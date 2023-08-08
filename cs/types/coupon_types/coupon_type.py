import graphene
from graphene_django import DjangoObjectType

from cs.models import Coupon


class CouponType(DjangoObjectType):
    class Meta:
        model = Coupon

    coupon_name = graphene.String()

    @staticmethod
    def resolve_coupon_name(root, __):
        return root.coupon_master.name
