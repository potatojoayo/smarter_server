import graphene

from cs.types.coupon_types.coupon_type import CouponType


class CouponsType(graphene.ObjectType):
    coupons = graphene.List(CouponType)
    total_count = graphene.Int()