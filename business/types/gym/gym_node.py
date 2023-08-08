import os

import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from base_classes import CountableConnectionBase
from business.models import Gym
from product.models import ProductMaster
from product.types.draft import DraftType
from product.types.draft.new_draft_type import NewDraftType
from product.types.product_master.product_master_type import ProductMasterType


class GymNode(DjangoObjectType):
    class Meta:
        model = Gym
        interfaces = (relay.Node,)
        filter_fields = {
            'date_created': ['lte', 'gte'],
            'membership__name': ['exact'],
            'name': ['icontains'],
            'agency_id': ['exact']
        }
        connection_class = CountableConnectionBase

    groups = graphene.List(graphene.String)
    smarter_money = graphene.Int()
    gym_id = graphene.Int()
    business_registration_certificate = graphene.String()
    drafts = graphene.List(NewDraftType)
    product_masters = graphene.List(ProductMasterType, category=graphene.String(), sub_category=graphene.String())
    membership = graphene.String()
    has_draft = graphene.Boolean()

    @staticmethod
    def resolve_has_draft(root, _):
        return root.user.drafts.exists()

    @staticmethod
    def resolve_product_masters(root, _, category='', sub_category=''):
        return ProductMaster.objects.filter(draft__user=root.user, category__name__contains=category, sub_category__name__contains=sub_category).distinct()

    @staticmethod
    def resolve_drafts(root, _):
        return root.user.new_drafts.filter(is_deleted=False)

    @staticmethod
    def resolve_membership(root, _):
        return root.membership.name

    @staticmethod
    def resolve_group(root, _):
        return root.groups.all()

    @staticmethod
    def resolve_gym_id(root, _):
        return root.id

    @staticmethod
    def resolve_business_registration_certificate(root, _):
        if root.business_registration_certificate:
            return os.environ.get("BASE_URL")+root.business_registration_certificate.url
