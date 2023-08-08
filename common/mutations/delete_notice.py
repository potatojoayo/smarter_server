import graphene

from common.models import Notice


class DeleteNotice(graphene.Mutation):
    class Arguments:
        notice_id = graphene.Int()

    success = graphene.Int()

    @classmethod
    def mutate(cls, _, __, notice_id):
        Notice.objects.filter(pk=notice_id).delete()

        return DeleteNotice(success=True)
