import graphene
from django.db import transaction

from product.types.draft import DraftType
from product.types.draft.draft_input_type import DraftInputType
from product.models import Draft, DraftImage, NewDraft
from product.types.draft.new_draft_input_type import NewDraftInputType
from product.types.draft.new_draft_type import NewDraftType


class CreateDraft(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int()
        draft = NewDraftInputType()

    success = graphene.Boolean()
    draft = graphene.Field(NewDraftType)

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, user_id, draft):

        draft_image = DraftImage.objects.create(image=draft.file)
        new_draft = NewDraft.objects.create(draft_image=draft_image,
                                            user_id=user_id,
                                            sub_category_id=draft.sub_category_id,
                                            price_work=draft.price_work,
                                            price_work_labor=draft.price_work_labor,
                                            memo=draft.memo,
                                            font=draft.font,
                                            thread_color=draft.thread_color,
                                            )

        return CreateDraft(success=True, draft=new_draft)
