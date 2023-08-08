import graphene

from calculate.models.agency_calculate import AgencyCalculate


class CompleteAgencyCalculation(graphene.Mutation):
    class Arguments:
        calculation_ids = graphene.List(graphene.Int)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, calculation_ids):
        print(calculation_ids)
        for calculation_id in calculation_ids:
            AgencyCalculate.objects.filter(pk=calculation_id).update(state="정산완료")
        return CompleteAgencyCalculation(success=True)
