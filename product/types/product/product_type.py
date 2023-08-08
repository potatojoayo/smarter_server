import graphene
from graphene_django import DjangoObjectType

from product.models import Product
from product.types.category.category_type import CategoryType


class ProductType(DjangoObjectType):

    class Meta:
        model = Product

    category = graphene.Field(CategoryType)
    price_product = graphene.Int()
    product_id = graphene.Int()

    @staticmethod
    def resolve_category(root, info):
        return root.product_master.category

    @staticmethod
    def resolve_price_product(root: Product, info):
        return root.product_master.price_gym + root.price_additional

    @staticmethod
    def resolve_product_id(root: Product, info):
        return root.id

