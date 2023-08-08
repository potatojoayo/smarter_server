import os

import graphene
from graphene_django import DjangoObjectType

from order.models.order_detail import OrderDetail
from order.types.work_type import WorkType
from product.types.draft.new_draft_type import NewDraftType


class OrderDetailType(DjangoObjectType):
    class Meta:
        model = OrderDetail

    recent_work = graphene.Field(WorkType)
    draft = graphene.Field(NewDraftType)
    order_detail_id = graphene.Int()
    thumbnail = graphene.String()

    @staticmethod
    def resolve_order_detail_id(root, _):
        return root.id

    @staticmethod
    def resolve_thumbnail(root: OrderDetail, _):
        return os.environ.get("BASE_URL")+root.product_master.thumbnail.url

    @staticmethod
    def resolve_recent_work(root, _):
        works = root.works.all().order_by('-date_created')
        if works.count() > 0:
            return works.first()

    @staticmethod
    def resolve_draft(root, _):
        return root.new_draft


