from graphene_django import DjangoObjectType
import graphene
from cs.models import ChangeRequestDetail
from product.types.product.product_type import ProductType


class ChangeDetailType(DjangoObjectType):
    class Meta:
        model = ChangeRequestDetail

    price_changed_product = graphene.Int()
    options = graphene.List(ProductType)
    product_name = graphene.String()
    changing_product = graphene.Field(ProductType)
    changed_product = graphene.Field(ProductType)

    @staticmethod
    def resolve_changing_product(root: ChangeRequestDetail, _):
        return root.changing_product

    @staticmethod
    def resolve_changed_product(root: ChangeRequestDetail, _):
        return root.changed_product

    @staticmethod
    def resolve_product_name(root: ChangeRequestDetail, _):
        return root.changed_product.product_master.name

    @staticmethod
    def resolve_options(root: ChangeRequestDetail, __):
        return root.changed_product.product_master.products.all().order_by('id')

    @staticmethod
    def resolve_price_changed_product(root: ChangeRequestDetail, __):
        return root.changed_product.product_master.price_gym + root.changed_product.price_additional