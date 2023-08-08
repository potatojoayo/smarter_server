import graphene
from graphene import relay


class SubcontractorStatisticsType(graphene.ObjectType):
    class Meta:
        interfaces = (relay.Node, )
    subcontractor_name = graphene.String()
    work_amount = graphene.Int()
    total_price_work = graphene.Int()
    total_price_work_labor = graphene.Int()
    date_from = graphene.String()
    date_to = graphene.String()


