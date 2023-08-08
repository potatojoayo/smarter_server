import os

import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from base_classes import CountableConnectionBase
from common.types import AddressType
from order.models import EasyOrder
from order.types.easy_order_file_type import EasyOrderFileType


class EasyOrderNode(DjangoObjectType):
    class Meta:
        model = EasyOrder
        interfaces = (relay.Node,)
        filter_fields = {
            'date_created': ['lte', 'gte'],
            'user__gym__name': ['icontains'],
            'user__phone': ['icontains'],
            'state': ['exact']
        }
        connection_class = CountableConnectionBase

    draft = graphene.String()
    easy_order_id = graphene.Int()
    default_address = graphene.Field(AddressType)
    addresses = graphene.List(AddressType)
    files = graphene.List(EasyOrderFileType)

    @staticmethod
    def resolve_files(root: EasyOrder, _):
        return root.files.all()

    @staticmethod
    def resolve_draft(root, _):
        if root.draft:
            return os.environ.get("BASE_URL")+root.draft.url

    @staticmethod
    def resolve_easy_order_id(root, _):
        return root.id
    @staticmethod
    def resolve_default_address(root, _):
        return root.user.addresses.get(default=True)

    @staticmethod
    def resolve_addresses(root, _):
        return root.user.addresses.filter(is_deleted=False)
