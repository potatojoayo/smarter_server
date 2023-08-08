import graphene
from product.models import DraftRequest
from product.types.draft_request.draft_request_type import DraftRequestType


class CreateDraftRequest(graphene.Mutation):

    draft_request = graphene.Field(DraftRequestType)
    created = graphene.Boolean()

    @classmethod
    def mutate(cls, _, info):
        user = info.context.user
        draft_requests = DraftRequest.objects.filter(user_id=user.id,
                                                    state='요청',)
        created = False
        if draft_requests.exists():
            draft_request = draft_requests.first()
        else:
            draft_request = DraftRequest.objects.create(user_id=user.id, state='요청')
            created = True
        """
        if created:
            send_notification(user=user, type="시안요청", product_names=product_master.name)
        """
        return CreateDraftRequest(draft_request=draft_request, created=created)

