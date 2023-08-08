import graphene
from graphene_django.filter import DjangoFilterConnectionField

from calculate.mutations.complete_agency_calculation import CompleteAgencyCalculation
from calculate.mutations.complete_subcontractor_calculation import CompleteSubcontractorCalculation
from calculate.types import AgencyCalculateNode, SubcontractorCalculateNode


class Query(graphene.ObjectType):
    agency_calculation = DjangoFilterConnectionField(AgencyCalculateNode)
    subcontractor_calculation = DjangoFilterConnectionField(SubcontractorCalculateNode)


class Mutation(graphene.ObjectType):
    complete_agency_calculation = CompleteAgencyCalculation.Field()
    complete_subcontractor_calculation = CompleteSubcontractorCalculation.Field()


schema = graphene.Schema(query=Query)
