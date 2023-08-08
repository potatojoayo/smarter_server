import graphene
from datetime import datetime

from django.db import transaction
from graphql import GraphQLError

from common.methods.send_notification import send_notification
from product.types.draft.draft_input_type import DraftInputType
from product.types.draft.new_draft_input_type import NewDraftInputType
from product.types.draft_request.draft_request_type import DraftRequestType
from product.models import DraftRequest, Draft, NewDraft


class CompleteDraftRequest(graphene.Mutation):
    class Arguments:
        draft_request_id = graphene.Int()
        drafts = graphene.List(NewDraftInputType)

    draft_request = graphene.Field(DraftRequestType)
    success = graphene.Boolean()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, draft_request_id, drafts):
        try:
            draft_request = DraftRequest.objects.get(pk=draft_request_id)
            sub_category = draft_request.product_master.sub_category
            for draft in drafts:
                NewDraft.objects.create(image=draft.file,
                                     user=draft_request.user,
                                     sub_category=sub_category,
                                     price_work=draft.price_work,
                                     price_work_labor=draft.price_work_labor,
                                     memo=draft.memo,
                                     font=draft.font,
                                     thread_color=draft.thread_color,
                                     draft_request=draft_request
                                     )

            draft_request.state = '완료'
            draft_request.date_finished = datetime.now()
            draft_request.save()
            # user = draft_request.user
            #send_notification(user=user, type="시안완료", product_names=draft_request.product_master.name)
            return CompleteDraftRequest(draft_request=draft_request, success=True)
        except GraphQLError as e:
            print(e)
            return CompleteDraftRequest(success=False)
