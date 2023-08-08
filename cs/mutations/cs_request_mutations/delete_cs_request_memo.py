import graphene
from cs.models import CsRequestMemos
from cs.types.cs_request_memo_type import CsRequestMemoType


class DeleteCsRequestMemo(graphene.Mutation):
    class Arguments:
        cs_request_memo_id = graphene.Int()

    success = graphene.Boolean()
    cs_request_memos = graphene.List(CsRequestMemoType)

    @classmethod
    def mutate(cls, _, __, cs_request_memo_id):
        try:
            memo = CsRequestMemos.objects.get(pk=cs_request_memo_id)
            cs_request = memo.cs_request
            memo.is_deleted = True
            memo.save()
            return DeleteCsRequestMemo(success=True,
                                       cs_request_memos=cs_request.request_memos.filter(is_deleted=False).order_by('date_created'))
        except Exception as e:
            import logging
            logger = logging.getLogger('myLog')
            logger.info(e)
            return DeleteCsRequestMemo(success=False)
