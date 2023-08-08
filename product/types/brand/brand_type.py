import graphene
from graphene_django import DjangoObjectType

from product.models import Brand
from product.types.product_master.product_master_type import ProductMasterType


class BrandType(DjangoObjectType):
    class Meta:
        model = Brand

    product_masters = graphene.List(ProductMasterType)

    @staticmethod
    def resolve_product_masters(root: Brand, _):
        return root.products.all()
