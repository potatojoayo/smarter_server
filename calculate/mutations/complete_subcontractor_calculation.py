import graphene

from calculate.models.subcontractor_calculate import SubcontractorCalculate


class CompleteSubcontractorCalculation(graphene.Mutation):
    class Arguments:
        calculation_ids = graphene.List(graphene.Int)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, calculation_ids):
        for calculation_id in calculation_ids:
            SubcontractorCalculate.objects.filter(pk=calculation_id).update(state="정산완료")
        return CompleteSubcontractorCalculation(success=True)
