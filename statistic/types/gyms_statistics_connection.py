from graphene import relay
import graphene

from statistic.types.gyms_statistics_type import GymsStatisticsType


class GymsStatisticsConnection(relay.Connection):
    class Meta:
        node = GymsStatisticsType

    total_count = graphene.Int()

    def resolve_total_count(self, _):
        return self.total_count

    class Edge:
        other = graphene.String()

