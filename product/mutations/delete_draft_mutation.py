import graphene

from product.models import Draft, Product, ProductMaster, Category, NewDraft


class DeleteDraftMutation(graphene.Mutation):
    class Arguments:
        deleted_category_id = graphene.Int()
        deleted_draft_id = graphene.Int()

    success = graphene.Boolean()
    @classmethod
    #product_master를 지우면 해당 product와 관련된 draft 다 삭제
    def mutate(cls, _, __, **kwargs):
        if 'deleted_product_master_id' in kwargs:
            deleting_category_id = kwargs.get("deleted_category_id")
            deleting_category = Category.objects.get(pk=deleting_category_id)
            NewDraft.objects.filter(sub_category=deleting_category).update(is_deleted=True)
    #해당 draft만 지움
        elif 'deleted_draft_id' in kwargs:
            deleting_draft_id = kwargs.get("deleted_draft_id")
            Draft.objects.filter(pk=deleting_draft_id).update(is_deleted=True)
        return DeleteDraftMutation(success=True)
