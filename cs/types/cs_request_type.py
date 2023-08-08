import graphene
from graphene_django import DjangoObjectType

from cs.models import CsRequest
from cs.types.cs_request_content_type import CsRequestContentType
from cs.types.cs_request_memo_type import CsRequestMemoType
from order.types.order_master_type import OrderMasterType


class CsRequestType(DjangoObjectType):
    class Meta:
        model = CsRequest

    gym = graphene.Field('business.types.gym.gym_type.GymType')
    gym_name = graphene.String()
    cs_request_id = graphene.Int()
    order_master = graphene.Field(OrderMasterType)
    order_master_id = graphene.Int()
    request_contents = graphene.List(CsRequestContentType, first=graphene.Int(), last=graphene.Int())
    total_count = graphene.Int()

    @staticmethod
    def resolve_order_master_id(root: CsRequest, __):
        return root.order_master_id

    @staticmethod
    def resolve_gym(root, __):
        return root.gym

    @staticmethod
    def resolve_total_count(root, __):
        return CsRequest.objects.all().count()

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
        return root.order_master

    @staticmethod
    def resolve_request_contents(root, __):
        return root.request_contents.filter(is_deleted=False, parent__isnull=True,).order_by('date_created')


