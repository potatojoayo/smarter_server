from graphene_django import DjangoObjectType

from cs.models import CouponIssueHistory
import graphene

class CouponIssueHistoryType(DjangoObjectType):
    class Meta:
        model = CouponIssueHistory

    referral_user_name = graphene.String()
    referral_user_phone = graphene.String()
    @staticmethod
    def resolve_referral_user_name(root, _):
        return root.coupon.referral_user.name if root.coupon.referral_user else None

    @staticmethod
    def resolve_referral_user_phone(root, _):
        return root.coupon.referral_user.phone if root.coupon.referral_user else None
