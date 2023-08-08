import graphene
from graphene_django import DjangoObjectType
from graphene import relay

from calculate.connection import AgencyCalculateConnection
from calculate.models.agency_calculate import AgencyCalculate


class AgencyCalculateNode(DjangoObjectType):
    class Meta:
        model = AgencyCalculate
        interfaces = (relay.Node, )
        filter_fields = {
            'date_from': ['gte'],
            'date_to': ['lte'],
            'agency__name': ['exact']
        }
        connection_class = AgencyCalculateConnection

    net_profit = graphene.Int()
    calculation_id = graphene.Int()

    @staticmethod
    def resolve_calculation_id(root, _):
        return root.id

    @staticmethod
    def resolve_net_profit(root, _):
        return root.net_profit

