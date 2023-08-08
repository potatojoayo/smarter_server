from graphene import relay
from graphene_django import DjangoObjectType

from base_classes import CountableConnectionBase
from order.models import OrderDetail


class OrderDetailNode(DjangoObjectType):
    class Meta:
        model = OrderDetail
        filter_fields = {
            "id": ['exact'],
            'order_master__date_created': ['lte', 'gte'],
            'order_master__user__gym__name': ['icontains'],
            'state': ['exact'],
            #'works__subcontractor__name': ['icontains']
        }
        interfaces = (relay.Node,)
        connection_class = CountableConnectionBase



