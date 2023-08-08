import graphene

from product.types.draft.draft_input_type import DraftInputType
from product.models import Draft, DraftImage


class UpdateDrafts(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int()
        drafts = graphene.List(DraftInputType)

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, user_id, drafts):
        for draft in drafts:
            if not draft.id:
                draft_image = DraftImage.objects.create(image=draft.file)
                Draft.objects.create(draft_image=draft_image,
                                     user_id=user_id,
                                     product_master_id=draft.product_master_id,
                                     price_work=draft.price_work,
                                     price_work_labor=draft.price_work_labor,
                                     memo=draft.memo,
                                     font=draft.font,
                                     thread_color=draft.thread_color,
                                     )
            else:
                old = Draft.objects.get(pk=draft.id)
                old.price_work_labor = draft.price_work_labor
                old.price_work = draft.price_work
                old.memo = draft.memo
                old.font = draft.font
                old.thread_color = draft.thread_color
                old.save()

        return UpdateDrafts(success=True)

