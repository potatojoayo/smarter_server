import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from base_classes import CountableConnectionBase
from inventory.models import InventoryOrderMaster
from inventory.types.inventory_order.inventory_order_detail_node import InventoryOrderDetailNode


class InventoryOrderMasterNode(DjangoObjectType):
    class Meta:
        model = InventoryOrderMaster
        interfaces = (relay.Node, )
        connection_class = CountableConnectionBase
        filter_fields = {
            'state': ['exact', 'in'],
            'date_created': ['lte', 'gte']
        }

    product_names = graphene.String()
    order_id = graphene.Int()
    details = DjangoFilterConnectionField(InventoryOrderDetailNode)
    price_total = graphene.Int()


    @staticmethod
    def resolve_price_total(root, _):
        return root.price_total

    @staticmethod
    def resolve_product_names(root, _):
        details = root.details.all()
        product_names = []
        names = ''
        for detail in details:
            product_name = detail.product.name
            product_names.append(product_name)
        product_names = list(set(product_names))
        for name in product_names:
            names += '{}, '.format(name)
        return names[:-2]

    @staticmethod
    def resolve_order_id(root, _):
        return root.id
