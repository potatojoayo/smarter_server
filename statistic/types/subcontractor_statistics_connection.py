from graphene import relay
import graphene

from statistic.types.subcontractor_statistics_type import SubcontractorStatisticsType


class SubcontractorStatisticsConnection(relay.Connection):
    class Meta:
        node = SubcontractorStatisticsType

    total_count = graphene.Int()

    def resolve_total_count(self, _):
        return self.total_count

    class Edge:
        other = graphene.String()

