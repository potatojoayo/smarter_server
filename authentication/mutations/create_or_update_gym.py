from datetime import datetime, timedelta

import graphene
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from authentication.models import User
from authentication.types import UserType
from authentication.types.user_input_type import UserInputType
from business.models import Gym, Agency
from business.types import GymType
from business.types.gym.gym_input_type import GymInputType
from django.contrib.auth.models import Group

from common.models import Address
from cs.methods.coupon_methods.issue_coupon import issue_coupon
from cs.methods.coupon_methods.issue_new_coupon import issue_new_coupon
from cs.methods.coupon_methods.issue_referral_coupon import issue_referral_coupon
from cs.models import CouponMaster, Coupon
from server.settings import logger


class CreateOrUpdateGym(graphene.Mutation):
    class Arguments:
        gym_user = UserInputType()
        is_active = graphene.Boolean(required=True)
        gym = GymInputType()
        agency_id = graphene.Int()
        agency_identification = graphene.String()
        referral_code = graphene.String()
        event = graphene.Boolean()

    gym_user = graphene.Field(UserType)
    gym = graphene.Field(GymType)
    success = graphene.Boolean(default_value=False)
    message = graphene.String()
    agency_not_found = graphene.Boolean(default_value=False)
    duplicated_identification = graphene.Boolean(default_value=False)
    duplicated_business_registration_number = graphene.Boolean(default_value=False)
    duplicated_phone = graphene.Boolean(default_value=False)

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, **kwargs):
        try:
            event = kwargs.get('event')
            referral_code = kwargs.get('referral_code')
            referral_user = None
            if referral_code:
                referral_user = User.objects.filter(phone=referral_code).first()
                if referral_user is None:
                    return CreateOrUpdateGym(success=False, message="추천인 번호에 해당되는 유저가 없습니다.")
            gym_user = kwargs.get('gym_user')
            is_active = kwargs.get('is_active')
            gym = kwargs.get('gym')
            if not gym['business_registration_certificate']:
                del gym['business_registration_certificate']
            agency_id = kwargs.get('agency_id') if 'agency_id' in kwargs else None
            agency_identification = kwargs.get('agency_identification')
            if agency_identification:
                try:
                    agency = Agency.objects.get(user__identification=agency_identification)
                    agency_id = agency.id
                except ObjectDoesNotExist:
                    return CreateOrUpdateGym(agency_not_found=True)

            if gym_user.id:
                new_gym_user = User.objects.get(pk=gym_user.id)
                User.objects.filter(pk=gym_user.id).update(**gym_user, is_active=is_active)
                if agency_id:
                    agency = Agency.objects.get(pk=agency_id)
                    Gym.objects.filter(user=new_gym_user).update(**gym, agency=agency)
                else:
                    Gym.objects.filter(user=new_gym_user).update(**gym)
                if event:
                    new_gym_user.is_participated_event = True
                    new_gym_user.save()
                    issue_coupon.delay(coupon_master_name='보안강화 이벤트 쿠폰', user_id=new_gym_user.id)

            else:
                phone_exists = User.objects.filter(phone=gym_user.phone).exists()
                if phone_exists:
                    return CreateOrUpdateGym(duplicated_phone=True)
                if User.objects.filter(identification=gym_user.identification).exists():
                    return CreateOrUpdateGym(duplicated_identification=True)
                new_gym_user = User.objects.create_user(**gym_user, is_active=is_active)
                new_gym_user.set_password(gym_user.password)
                new_gym_user.save()
                group = Group.objects.get(name='체육관')
                new_gym_user.groups.add(group)
                new_gym = Gym.objects.create(user=new_gym_user, **gym)
                ## 신규가입 쿠폰
                issue_coupon.delay(coupon_master_name="신규가입쿠폰", user_id=new_gym_user.id)
                ## 추천인 쿠폰
                if referral_user:
                    issue_referral_coupon.delay(referral_user_id=referral_user.id, nominee=new_gym.id)
                if agency_id:
                    agency = Agency.objects.get(pk=agency_id)
                    new_gym.agency = agency
                    new_gym.save()
                Address.objects.create(user=new_gym_user, name='체육관',
                                       address=new_gym.address,
                                       receiver=new_gym_user.name,
                                       phone=new_gym_user.phone,
                                       zip_code=new_gym.zip_code,
                                       detail_address=new_gym.detail_address,
                                       default=True
                                       )
            return CreateOrUpdateGym(success=True, agency_not_found=False)
        except Exception as e:
            logger.info('회원가입 실패')
            logger.info(e)
            return CreateOrUpdateGym(success=False, agency_not_found=False)
