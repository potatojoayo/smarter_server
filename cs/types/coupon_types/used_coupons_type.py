import graphene

from cs.types.coupon_types.coupon_use_history_type import CouponUseHistoryType


class UsedCouponsType(graphene.ObjectType):
    used_coupons_histories = graphene.List(CouponUseHistoryType)
    total_count = graphene.Int()
