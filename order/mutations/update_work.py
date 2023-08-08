import graphene

from order.models import Work


class UpdateWork(graphene.Mutation):
    class Arguments:
        work_id = graphene.Int()
        memo = graphene.String()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, work_id, memo):
        Work.objects.filter(pk=work_id).update(memo=memo)
        return UpdateWork(success=True)
