from graphene import relay
import graphene

from statistic.types.product_statistics_type import ProductStatisticsType


class ProductStatisticsConnection(relay.Connection):
    class Meta:
        node = ProductStatisticsType

    total_count = graphene.Int()

    def resolve_total_count(self, _):
        return self.total_count

    class Edge:
        other = graphene.String()

