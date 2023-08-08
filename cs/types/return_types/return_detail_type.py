from graphene_django import DjangoObjectType

from cs.models import ReturnRequestDetail
import graphene


class ReturnDetailType(DjangoObjectType):
    class Meta:
        model = ReturnRequestDetail

    product_master_name = graphene.String()
    color = graphene.String()
    size = graphene.String()

    @staticmethod
    def resolve_product_master_name(root, __):
        return root.order_detail.product_master.name

    @staticmethod
    def resolve_color(root, __):
        return root.order_detail.product.color

    @staticmethod
    def resolve_size(root, __):
        return root.order_detail.product.size
