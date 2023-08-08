import graphene

from gym_student.models import AuditionDetail


class DeleteAuditionDetail(graphene.Mutation):
    class Arguments:
        audition_detail_id = graphene.Int()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, audition_detail_id):
        audition_detail = AuditionDetail.objects.get(pk=audition_detail_id)
        audition_detail.delete()

        return DeleteAuditionDetail(success=True)