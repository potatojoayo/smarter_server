import graphene
from graphene_django import DjangoObjectType

from cs.models import CouponMaster, Coupon
from cs.types.coupon_types.coupon_type import CouponType
from datetime import datetime, timedelta


class CouponMasterType(DjangoObjectType):
    class Meta:
        model = CouponMaster
    total_issued_count = graphene.Int(source='total_issued_count')
    all_coupons = graphene.List(CouponType, page=graphene.Int(), coupon_number=graphene.String(), gym_name=graphene.String(),
                            start=graphene.String(), end=graphene.String())
    used_coupons = graphene.List(CouponType, page=graphene.Int(), coupon_number=graphene.String(), gym_name=graphene.String(),
                            start=graphene.String(), end=graphene.String())

    coupons = graphene.List(CouponType)

    @staticmethod
    def resolve_coupons(root, __):
        return root.coupons.all()
    
    @staticmethod
    def resolve_all_coupons(_, __, page, coupon_number, gym_name, start, end):
        date_created_start = datetime.strptime(start, '%Y-%m-%d').date()
        date_created_end = datetime.strptime(end, '%Y-%m-%d').date() + timedelta(days=1)
        return Coupon.objects.filter(coupon_number__icontains=coupon_number,
                                     user__gym__name__icontains=gym_name,
                                     date_created__lte=date_created_end,
                                     date_created__gte=date_created_start)[10*(page-1):(10*page-1)]

    @staticmethod
    def resolve_used_coupons(_, __, page, coupon_number, gym_name, start, end):
        date_created_start = datetime.strptime(start, '%Y-%m-%d').date()
        date_created_end = datetime.strptime(end, '%Y-%m-%d').date() + timedelta(days=1)
        return Coupon.objects.filter(## 사용한거 필터링
                                     coupon_number__icontains=coupon_number,
                                     user__gym__name__icontains=gym_name,
                                     date_created__lte=date_created_end,
                                     date_created__gte=date_created_start)[10 * (page - 1):(10 * page - 1)]

