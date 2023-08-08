import graphene
from graphene import relay


class SubcontractorCalculateConnection(relay.Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int()
    total_price_work = graphene.Int()
    total_work_amount = graphene.Int()
    total_price_work_labor = graphene.Int()

    def resolve_total_count(self, info, **kwargs):
        return self.iterable.count()

    def resolve_total_price_work(self, _, **kwargs):
        total = 0
        for cal in self.iterable:
            total += cal.total_price_work
        return total

    def resolve_total_price_work_labor(self, _, **kwargs):
        total = 0
        for cal in self.iterable:
            total += cal.total_price_work_labor
        return total

    def resolve_total_work_amount(self, _, **kwargs):
        total = 0
        for cal in self.iterable:
            total += cal.work_amount
        return total


