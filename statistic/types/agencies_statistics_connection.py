from graphene import relay
import graphene

from statistic.types.agencies_statistics_type import AgenciesStatisticsType, FirstInnerItem


class AgenciesStatisticsConnection(relay.Connection):
    class Meta:
        node = AgenciesStatisticsType

    total_count = graphene.Int()

    def resolve_total_count(self, _):
        return self.total_count

    class Edge:
        other = graphene.String()

