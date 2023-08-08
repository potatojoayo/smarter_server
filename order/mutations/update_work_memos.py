import graphene

from order.models import Work


class UpdateWorkMemos(graphene.Mutation):
    class Arguments:
        work_id = graphene.Int()
        memo_by_subcontractor = graphene.String()
        memo_by_admin = graphene.String()
        memo_by_pre_worker = graphene.String()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, work_id, memo_by_subcontractor=None,
               memo_by_admin=None, memo_by_pre_worker=None,):
        Work.objects.filter(pk=work_id).update(memo_by_subcontractor=memo_by_subcontractor,
                                               memo_by_admin=memo_by_admin,
                                               memo_by_pre_worker=memo_by_pre_worker)
        return UpdateWorkMemos(success=True)
