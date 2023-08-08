import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from base_classes import CountableConnectionBase
from business.types import GymType
from cs.models import CsRequest
from cs.types.cs_request_content_type import CsRequestContentType
from order.types.order_master_type import OrderMasterType


class CsRequestNode(DjangoObjectType):
    class Meta:
        model = CsRequest
        interfaces = (relay.Node, )
        filter_fields = {'gym__name': ['icontains'],
                         'gym__user__name': ['icontains'],
                         'gym__user__phone': ['icontains'],
                         'cs_state': ['exact'],
                         'date_created': ['lte', 'gte'],}
        connection_class = CountableConnectionBase

    gym = graphene.Field(GymType)
    gym_name = graphene.String()
    cs_request_id = graphene.Int()
    order_master = graphene.Field(OrderMasterType)
    cs_request_contents = graphene.List(CsRequestContentType, first=graphene.Int(), last=graphene.Int())

    @staticmethod
    def resolve_gym_name(root, __):
        return root.gym.name

    @staticmethod
    def resolve_cs_request_id(root, __):
        return root.id

    @staticmethod
    def resolve_customer(root, __):
        return root.gym

    @staticmethod
    def resolve_order_master(root, __):
        return root.order_master.filter(is_deleted=False)

    @staticmethod
    def resolve_cs_request_contents(root, __, first, last):
        return root.reqeust_contents.filter(is_deleted=False).order_by('id')[first:last]


