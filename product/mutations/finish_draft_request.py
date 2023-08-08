import graphene

from product.models import DraftRequest


class FinishDraftRequest(graphene.Mutation):
    class Arguments:
        draft_request_id = graphene.Int()

    success = graphene.Boolean()
    message = graphene.String()

    @classmethod
    def mutate(cls, _, __, draft_request_id):
        try:
            draft_request = DraftRequest.objects.get(pk=draft_request_id)
            draft_request.state = "완료"
            draft_request.save()
            return FinishDraftRequest(success=True, message="완료되었습니다.")
        except Exception as e:
            import logging
            logger = logging.getLogger('myLog')
            logger.info(e)
            return FinishDraftRequest(success=False, message="오류가 발생하였습니다. 개발팀에 문의해주세요")
