import graphene
from django.db import transaction
from graphene_file_upload.scalars import Upload

from product.models import NewDraft, Category
from product.models.draft_size import DraftSize
from product.types.draft.new_draft_input_type import NewDraftInputType
from product.types.draft.new_draft_type import NewDraftType
from product.types.size.draft_size_input_type import DraftSizeInputType
from server.settings import logger


class CreateNewDraft(graphene.Mutation):
    class Arguments:
        draft = NewDraftInputType(required=True)
        file = Upload()
        user_id = graphene.Int()
        subcategory_name = graphene.String()
        sizes = graphene.List(DraftSizeInputType)

    success = graphene.Boolean(default_value=False)

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, draft, user_id, subcategory_name, file, sizes):
        try:
            new_draft = NewDraft.objects.create(**draft, user_id=user_id)
            new_draft.sub_category = Category.objects.get(name=subcategory_name)
            new_draft.image = file
            new_draft.save()
            for size in sizes:
                DraftSize.objects.create(new_draft=new_draft, **size)
            return CreateNewDraft(success=True)
        except Exception as e:
            logger.info('create_new_draft_error')
            logger.info(e)
            logger.info('draft : '+str(draft))
            logger.info('user_id : '+str(user_id))
            logger.info('subcategory_name : '+str(subcategory_name))
            logger.info('sizes : '+str(sizes))
            return CreateNewDraft(success=False)

