import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from base_classes import CountableConnectionBase
from order.models import Work
from order.types.order_detail_type import OrderDetailType
from order.types.order_master_node import OrderMasterNode
from product.types.draft.new_draft_type import NewDraftType


class WorkNode(DjangoObjectType):

    class Meta:
        model = Work
        interfaces = (relay.Node, )
        filter_fields = {
            'subcontractor__name': ['exact', 'icontains'],
            'date_created': ['lte', 'gte'],
            'details__state': ['in'],
            'state': ['exact'],
            'subcontractor__is_out_working': ['exact']
        }
        connection_class = CountableConnectionBase

    # order_master = relay.Node.Field(OrderMasterNode)
    work_id = graphene.Int()
    product_names = graphene.List(graphene.String)
    drafts = graphene.List(NewDraftType)
    details = graphene.List(OrderDetailType)

    @staticmethod
    def resolve_details(root, _):
        return root.details.all().order_by('product_id')

    @staticmethod
    def resolve_drafts(root: Work, _):
        return root.drafts

    @staticmethod
    def resolve_work_id(root, _):
        return root.id

    @staticmethod
    def resolve_product_names(root, _):
        return root.product_names
