import graphene

from product.models import NewDraft


class DeleteDrafts(graphene.Mutation):
    class Arguments:
        deleted_draft_ids = graphene.List(graphene.Int)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, deleted_draft_ids):
        for deleted_id in deleted_draft_ids:
            NewDraft.objects.filter(pk=deleted_id).update(is_deleted=True)

        return DeleteDrafts(success=True)