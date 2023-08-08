import graphene

from cs.types.coupon_types.coupon_master_type import CouponMasterType


class CouponMastersType(graphene.ObjectType):
    coupon_masters = graphene.List(CouponMasterType)
    total_count = graphene.Int()