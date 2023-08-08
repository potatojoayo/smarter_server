import graphene
from graphene_django import DjangoObjectType

from order.models import Work



class WorkType(DjangoObjectType):
    class Meta:
        model = Work

    details = graphene.List('order.types.order_detail_type.OrderDetailType')

    @staticmethod
    def resolve_details(root, _):
        from order.types.order_detail_type import OrderDetailType
        return root.details.all().order_by('product_id')
