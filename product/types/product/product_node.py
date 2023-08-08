import os

import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from base_classes import CountableConnectionBase
from product.models import Product


class ProductNode(DjangoObjectType):

    class Meta:
        model = Product
        interfaces = (relay.Node,)
        filter_fields = {
            'name': ['icontains'],
            'product_master__category__name': ['exact'],
            'product_master__sub_category__name': ['exact'],
            'product_master__brand__name': ['exact'],
        }
        connection_class = CountableConnectionBase

    product_id = graphene.Int()

    @staticmethod
    def resolve_product_id(root, _):
        return root.id
