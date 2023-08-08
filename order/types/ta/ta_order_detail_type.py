import os

import graphene
from graphene_django import DjangoObjectType

from order.models import TaOrderDetail


class TaOrderDetailType(DjangoObjectType):
    class Meta:
        model = TaOrderDetail

    product_image = graphene.String()

    @staticmethod
    def resolve_product_image(root: TaOrderDetail, _):
        return os.environ.get("BASE_URL")+root.order_detail.product_master.thumbnail.url

    product_name = graphene.String()

    @staticmethod
    def resolve_product_name(root: TaOrderDetail, _):
        return root.order_detail.product_master.name

    color = graphene.String()

    @staticmethod
    def resolve_color(root: TaOrderDetail, _):
        return root.order_detail.product.color

    size = graphene.String()

    @staticmethod
    def resolve_size(root: TaOrderDetail, _):
        return root.order_detail.product.size

    price_gym = graphene.Int()

    @staticmethod
    def resolve_price_gym(root: TaOrderDetail, _):
        return root.order_detail.product.price_additional + root.order_detail.product_master.price_gym

    price_work = graphene.Int()

    @staticmethod
    def resolve_price_work(root: TaOrderDetail, _):
        return root.order_detail.new_draft.price_work if root.order_detail.new_draft else 0

    quantity = graphene.Int()

    @staticmethod
    def resolve_quantity(root: TaOrderDetail, _):
        return root.order_detail.quantity
