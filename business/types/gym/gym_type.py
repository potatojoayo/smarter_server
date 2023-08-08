import os
from datetime import datetime, timedelta

import graphene
from graphene_django import DjangoObjectType

from authentication.models import User
from business.models import Gym, GymMonthlyPurchasedAmount
from cs.types.addresses_type import AddressesType
from cs.types.cs_order_masters_type import CsOrderMastersType
from cs.types.cs_requests_type import CsRequestsType
from cs.types.drafts_type import DraftsType
from cs.types.smarter_money_histories_type import SmarterMoneyHistoriesType


class GymType(DjangoObjectType):
    class Meta:
        model = Gym
        fields = '__all__'

    agency = graphene.Field('business.types.agency.AgencyType')

    ## 추가

    smarter_money = graphene.Int()
    gym_id = graphene.Int()
    business_registration_certificate = graphene.String()

    ## cs

    cs_requests = graphene.Field(CsRequestsType, page=graphene.Int())
    order_masters = graphene.Field(CsOrderMastersType, page=graphene.Int(), exclude_states=graphene.List(graphene.String))
    smarter_money_histories = graphene.Field(SmarterMoneyHistoriesType, page=graphene.Int())
    addresses = graphene.Field(AddressesType, page=graphene.Int())
    drafts = graphene.Field(DraftsType, page=graphene.Int())

    prev_month_purchased_amount = graphene.Int()

    @staticmethod
    def resolve_prev_month_purchased_amount(root: Gym, __):
        now = datetime.now().replace(day=1)
        prev_month = now - timedelta(days=1)
        business_registration_certificate = graphene.String()
        prev_month = prev_month.replace(day=1)
        year = prev_month.year
        month = prev_month.month
        date = datetime(year=year, month=month, day=1)
        monthly_purchased_amount, _ = GymMonthlyPurchasedAmount.objects.get_or_create(gym=root, date=date)
        return monthly_purchased_amount.amount

    @staticmethod
    def resolve_drafts(root: Gym, __, page):
        user = root.user
        drafts = user.new_drafts.filter(is_deleted=False).order_by('-date_created')
        return DraftsType(drafts=drafts[10*(page-1): 10*page],
                          total_count = drafts.count())


    @staticmethod
    def resolve_smarter_money(root, _):
        return root.user.wallet.balance

    @staticmethod
    def resolve_addresses(root: Gym, __, page):
        user = root.user
        addresses = user.addresses.filter(is_deleted=False).order_by('-id')
        return AddressesType(addresses=addresses[10*(page-1): 10*page],
                             total_count = addresses.count())
    @staticmethod
    def resolve_smarter_money_histories(root, __, page):
        user = root.user
        smarter_money_histories = user.wallet.history.all().order_by('-date_created')
        return SmarterMoneyHistoriesType(smarter_money_histories=smarter_money_histories[10*(page-1): 10*page],
                                         total_count = smarter_money_histories.count())
    @staticmethod
    def resolve_order_masters(root, __, page, exclude_states=None):
        if not exclude_states:
            exclude_states = []
        user: User = root.user
        order_masters = user.orders.filter(is_deleted=False).exclude(
            details__state__in=exclude_states
        ).order_by('-date_created')
        return CsOrderMastersType(order_masters=order_masters[10*(page-1): 10*page],
                                  total_count = order_masters.count())

    @staticmethod
    def resolve_cs_requests(root, __, page):
        cs_requests = root.cs_requests.filter(gym=root, is_deleted=False).order_by('-date_requested')
        return CsRequestsType(cs_requests=cs_requests[5*(page-1): 5*page],
                              total_count=cs_requests.count())
    @staticmethod
    def resolve_agency(root, info):
        return root.agency

    @staticmethod
    def resolve_business_registration_certificate(root, _):
        if root.business_registration_certificate:
            return os.environ.get("BASE_URL")+root.business_registration_certificate.url

