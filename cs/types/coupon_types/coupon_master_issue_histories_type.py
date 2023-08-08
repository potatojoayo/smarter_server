import graphene

from cs.types.coupon_types.coupon_master_issue_history_type import CouponMasterIssueHistoryType


class CouponMasterIssueHistoriesType(graphene.ObjectType):

    coupon_master_issue_histories = graphene.List(CouponMasterIssueHistoryType)
    total_count = graphene.Int()

