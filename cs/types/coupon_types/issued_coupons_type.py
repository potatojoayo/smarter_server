import graphene

from cs.types.coupon_types.coupon_issue_history_type import CouponIssueHistoryType


class IssuedCouponsType(graphene.ObjectType):
    issued_coupons_histories = graphene.List(CouponIssueHistoryType)
    total_count = graphene.Int()
