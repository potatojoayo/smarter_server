import graphene

from cs.models import CsRequestContents
from cs.types.cs_request_content_type import CsRequestContentType
from server.settings import logger


class UpdateContentReply(graphene.Mutation):
    class Arguments:
        reply_id = graphene.Int()
        contents = graphene.String()

    success = graphene.Boolean()
    reply = graphene.Field(CsRequestContentType)
    @classmethod
    def mutate(cls, _, __, reply_id, contents):
        try:
            reply = CsRequestContents.objects.get(pk=reply_id)
            reply.contents = contents
            reply.save()
            return UpdateContentReply(success=True, reply=reply)
        except Exception as e:
            logger.info("update_content_reply")
            logger.info('reply_id : '+str(reply_id))
            logger.info(e)
            return UpdateContentReply(success=False)