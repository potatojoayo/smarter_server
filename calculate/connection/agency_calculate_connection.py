import graphene
from graphene import relay


class AgencyCalculateConnection(relay.Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int()
    total_sell = graphene.Int()
    total_profit = graphene.Int()
    total_price_platform = graphene.Int()
    total_net_profit = graphene.Int()

    def resolve_total_count(self, info, **kwargs):
        return self.iterable.count()

    def resolve_total_sell(self, _, **kwargs):
        total = 0
        for cal in self.iterable:
            total += cal.agency_total_sell
        return total

    def resolve_total_profit(self, _, **kwargs):
        total = 0
        for cal in self.iterable:
            total += cal.price_profit
        return total

    def resolve_total_price_platform(self, _, **kwargs):
        total = 0
        for cal in self.iterable:
            total += cal.price_platform
        return total

    def resolve_total_net_profit(self, _, **kwargs):
        total = 0
        for cal in self.iterable:
            total += cal.net_profit
        return total

