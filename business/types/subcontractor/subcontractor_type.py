import graphene
from graphene_django import DjangoObjectType

from business.models import Subcontractor


class SubcontractorType(DjangoObjectType):

    class Meta:
        model = Subcontractor
        fields='__all__'

    daily_cumulative_work = graphene.Int()


    @staticmethod
    def resolve_cumulative_work(root, _):
        return root.daily_cumulative_work
