import graphene

from gym_student.models import AuditionDetail
from gym_student.types.audition_detail.audition_detail_type import AuditionDetailType


class AuditionDetailPass(graphene.Mutation):
    class Arguments:
        audition_detail_id = graphene.Int()
        did_pass = graphene.Boolean()
        memo = graphene.String(default_value=None)

    success = graphene.Boolean()
    detail = graphene.Field(AuditionDetailType)

    @classmethod
    def mutate(cls, _, __, audition_detail_id, memo, did_pass=None):
        audition_detail = AuditionDetail.objects.get(pk=audition_detail_id)
        audition_detail.did_pass = did_pass
        if did_pass:
            audition_detail.student.level = audition_detail.audition_master.next_level
            audition_detail.student.save()
        audition_detail.memo = memo
        audition_detail.save()

        return AuditionDetailPass(success=True, detail=audition_detail)
