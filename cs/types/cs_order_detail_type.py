from graphene_django import DjangoObjectType
import graphene
from order.models import OrderDetail


class CsOrderDetailType(DjangoObjectType):
    class Meta:
        model = OrderDetail


    product_master_name = graphene.String()
    price_gym = graphene.Int()
    color = graphene.String()
    size = graphene.String()
    price_additional = graphene.Int()
    price_work = graphene.Int()
    colors = graphene.List(graphene.String)
    sizes = graphene.List(graphene.String)


    @staticmethod
    def resolve_product_master_name(root, __):
        return root.product_master.name

    @staticmethod
    def resolve_price_gym(root, __):
        return root.product_master.price_gym

    @staticmethod
    def resolve_color(root, __):
        return root.product.color

    @staticmethod
    def resolve_size(root, __):
        return root.product.size

    @staticmethod
    def resolve_additional_price(root, __):
        return root.product.price_additional

    @staticmethod
    def resolve_price_work(root, __):
        if root.new_draft:
            price_work = root.new_draft.price_work
        else:
            price_work = root.new_draft.price_work
        return price_work

    @staticmethod
    def resolve_colors(root, __):
        return root.product_master.colors

    @staticmethod
    def resolve_sizes(root, __):
        return root.product_master.sizes