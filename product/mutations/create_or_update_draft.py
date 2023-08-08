import graphene

from authentication.models import User
from product.models import Draft, ProductMaster, Category, NewDraft
from product.types.draft.new_draft_input_type import NewDraftInputType
from product.types.draft.new_draft_type import NewDraftType


class CreateOrUpdateDraft(graphene.Mutation):
    class Arguments:
        draft = NewDraftInputType()
        user_id = graphene.Int()
        sub_category = graphene.String()

    draft = graphene.Field(NewDraftType)
    success = graphene.Boolean(default_value=False)

    @classmethod
    def mutate(cls, _, __, draft, user_id, sub_category):
        print(draft)
        user = User.objects.get(pk=user_id)
        sub_category = Category.objects.get(name=sub_category)
        if draft.id:
            new_draft = NewDraft.objects.get(pk=draft.id)
            new_draft.sub_category = sub_category
            new_draft.price_work = draft.price_work
            new_draft.price_work_labor = draft.price_work_labor
            new_draft.memo = draft.memo
            new_draft.font = draft.font
            new_draft.thread_color = draft.thread_color
            new_draft.printing = draft.printing
            if draft.image:
                new_draft.image = draft.image
            new_draft.save()
        else:
            new_draft = NewDraft.objects.create(user=user, sub_category=sub_category, **draft)
        return CreateOrUpdateDraft(draft=new_draft, success=True)
