import graphene
from django.db import transaction

from authentication.models import User
from product.models import ProductMaster, DraftImage, Draft, Category, NewDraft
from product.types.draft.draft_input_type import DraftInputType


class CreateMultipleDrafts(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int()
        draft = DraftInputType()
        category_name = graphene.String()
        sub_category_name = graphene.String()

    success = graphene.Boolean()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, user_id, draft, category_name, sub_category_name):
        user = User.objects.get(pk=user_id)
        sub_category = Category.objects.get(parent__name=category_name, name=sub_category_name)
        draft_image = DraftImage.objects.create(image=draft.file)
        NewDraft.objects.create(sub_category=sub_category,
                                draft_image=draft_image,
                                user=user,
                                price_work=draft.price_work,
                                price_work_labor=draft.price_work_labor,
                                memo=draft.memo,
                                font=draft.font,
                                thread_color=draft.thread_color)
        return CreateMultipleDrafts(success=True)