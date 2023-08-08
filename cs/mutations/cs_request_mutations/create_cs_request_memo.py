
import graphene

from cs.models import CsRequest, CsRequestMemos
from cs.types.cs_request_memo_type import CsRequestMemoType


class CreateCsRequestMemo(graphene.Mutation):
    class Arguments:
        cs_request_id = graphene.Int()
        memo = graphene.String()

    success = graphene.Boolean()
    cs_request_memos = graphene.List(CsRequestMemoType)

    @classmethod
    def mutate(cls, _, __, cs_request_id, memo):
        try:
            cs_request = CsRequest.objects.get(pk=cs_request_id)
            CsRequestMemos.objects.create(cs_request=cs_request,
                                          contents=memo)
            return CreateCsRequestMemo(success=True,
                                       cs_request_memos=cs_request.request_memos.filter(is_deleted=False).order_by('date_created'))
        except Exception as e:
            import logging
            logger = logging.getLogger('myLog')
            logger.info(e)
            return CreateCsRequestMemo(success=False)

