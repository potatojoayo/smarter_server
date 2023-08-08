import graphene
from graphene_django import DjangoObjectType
from graphene import relay

from calculate.connection import SubcontractorCalculateConnection
from calculate.models.subcontractor_calculate import SubcontractorCalculate


class SubcontractorCalculateNode(DjangoObjectType):
    class Meta:
        model = SubcontractorCalculate
        interfaces = (relay.Node, )
        filter_fields = {
            'date_from': ['gte'],
            'date_to': ['lte'],
            'subcontractor__name': ['exact'],
            'subcontractor__is_out_working': ['exact'],
            'subcontractor__is_pre_working': ['exact'],
        }
        connection_class = SubcontractorCalculateConnection

    calculation_id = graphene.Int()

    @staticmethod
    def resolve_calculation_id(root, _):
        return root.id
