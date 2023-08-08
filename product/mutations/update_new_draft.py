import graphene
from django.db import transaction
from graphene_file_upload.scalars import Upload

from product.models import NewDraft, DraftSize
from product.types.draft.new_draft_input_type import NewDraftInputType
from product.types.size.draft_size_input_type import DraftSizeInputType
from server.settings import logger


class UpdateNewDraft(graphene.Mutation):
    class Arguments:
        draft_id = graphene.Int(required=True)
        draft = NewDraftInputType(required=True)
        file = Upload()
        sizes = graphene.List(DraftSizeInputType)

    success = graphene.Boolean(default_value=False)

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, draft_id, draft, sizes, file=None):
        try:
            old_draft = NewDraft.objects.get(pk=draft_id)
            NewDraft.objects.filter(pk=draft_id).update(**draft)
            if file:
                old_draft.image = file
                old_draft.save()
            for size in sizes:
                size_id = size.pop('id')
                DraftSize.objects.filter(pk=size_id).update(**size)
            return UpdateNewDraft(success=True)
        except Exception as e:
            logger.info('update_new_draft_error')
            logger.info(e)
            return UpdateNewDraft(success=False)


