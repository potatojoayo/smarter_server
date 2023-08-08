import os

import graphene
from graphene_django import DjangoObjectType

from cs.types.change_types.change_detail_type import ChangeDetailType
from cs.types.change_types.change_request_type import ChangeRequestType
from order.models import Delivery
from order.types.order_detail_type import OrderDetailType
from order.types.order_master_type import OrderMasterType


class DeliveryType(DjangoObjectType):
    class Meta:
        model = Delivery

    order_details = graphene.List(OrderDetailType)
    order_master = graphene.Field(OrderMasterType)
    photo = graphene.String()
    change_details = graphene.List(ChangeDetailType)
    change = graphene.Field(ChangeRequestType)
    @staticmethod
    def resolve_order_details(root, _):
        return root.order_details.all()

    @staticmethod
    def resolve_order_master(root, _):
        return root.order_details.first().order_master

    @staticmethod
    def resolve_photo(root, _):
        if root.photo:
            return os.environ.get("BASE_URL")+root.photo.url
    @staticmethod
    def resolve_change_details(root, __):
        return root.change_details.all()

    @staticmethod
    def resolve_change(root, __):
        return root.change_details.first().cs_request_change