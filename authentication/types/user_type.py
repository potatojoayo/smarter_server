import os
from datetime import datetime

import graphene
from graphene_django import DjangoObjectType

from authentication.models import User
from business.types import GymType
from business.types.agency.agency_type import AgencyType
from business.types.subcontractor.subcontractor_type import SubcontractorType
from cs.types.coupon_types.coupon_type import CouponType
from gym_student.types.parent_type import ParentType


class UserType(DjangoObjectType):

    gym = graphene.Field(GymType)
    agencies = graphene.List(AgencyType)
    subcontractors = graphene.List(SubcontractorType)
    group = graphene.String()
    parent = graphene.Field(ParentType)
    coupons = graphene.List(CouponType)
    profile_image = graphene.String()

    class Meta:
        model = User
        fields = '__all__'

    @staticmethod
    def resolve_profile_image(root: User, _):
        if root.profile_image:
            return os.environ.get("BASE_URL")+root.profile_image.url
        return None

    @staticmethod
    def resolve_coupons(root: User, _):
        return root.coupons.filter(date_used__isnull=True, end_of_use__gt=datetime.now())

    @staticmethod
    def resolve_group(root, info):
        try:
            groups = root.groups.all()
            for group in groups:
                if group.name=='체육사':
                    return '체육사'
            return root.groups.first().name
        except:
            return

    @staticmethod
    def resolve_gyms(root, info):
        return root.gym

    @staticmethod
    def resolve_parent(root, _):
        return root.parent

    @staticmethod
    def resolve_agencies(root, info):
        return root.agencys.all()

    @staticmethod
    def resolve_subcontractors(root,info):
        return root.subcontractors.all()

    # @staticmethod
    # def resolve_addresses(root, _):
    #     return root.addresses.all()



