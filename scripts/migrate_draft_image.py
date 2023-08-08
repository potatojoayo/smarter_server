from product.models import Draft, DraftImage


def run():

    drafts = Draft.objects.all()
    for draft in drafts:
        di = DraftImage.objects.create(image=draft.image)
        draft.draft_image = di
        draft.save()

