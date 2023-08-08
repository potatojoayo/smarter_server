import graphene
from graphene_django import DjangoObjectType
from cs.models import CouponMasterIssueHistory
from cs.types.coupon_types.coupon_master_type import CouponMasterType


class CouponMasterIssueHistoryType(DjangoObjectType):
    class Meta:
        model = CouponMasterIssueHistory

    coupon_master = graphene.Field(CouponMasterType)

    @staticmethod
    def resolve_coupon_master(root: CouponMasterIssueHistory, _):
        return root.coupon_master

