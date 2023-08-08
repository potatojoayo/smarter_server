import graphene

from cs.models import CsRequestContents
from server.settings import logger


class DeleteContentReply(graphene.Mutation):
    class Arguments:
        content_id = graphene.Int()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, content_id):
        try:
            content = CsRequestContents.objects.get(pk=content_id)
            content.delete()
            return DeleteContentReply(success=True)
        except Exception as e:
            logger.info('delete_content_reply_error')
            logger.info('content_id : '+str(content_id))
            logger.info(e)
            return DeleteContentReply(success=False)