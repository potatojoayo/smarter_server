import graphene
from graphene_file_upload.scalars import Upload

from product.models import Draft, DraftImage


class UpdateDraftImage(graphene.Mutation):
    class Arguments:
        draft_id = graphene.Int()
        image = Upload()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, draft_id, image):
        new_draft_image = DraftImage.objects.create(image=image)
        draft = Draft.objects.get(pk=draft_id)
        draft.draft_image = new_draft_image
        draft.save()

        return UpdateDraftImage(success=True)
