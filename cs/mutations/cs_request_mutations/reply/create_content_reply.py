import graphene

from cs.models import CsRequestContents
from cs.types.cs_request_content_type import CsRequestContentType
from server.settings import logger


class CreateContentReply(graphene.Mutation):
    class Arguments:
        parent_id = graphene.Int()
        contents = graphene.String()

    success = graphene.Boolean()
    reply = graphene.Field(CsRequestContentType)


    @classmethod
    def mutate(cls, _, __, parent_id, contents):
        try:
            parent = CsRequestContents.objects.get(pk=parent_id)
            reply = CsRequestContents.objects.create(cs_request=parent.cs_request,
                                             contents=contents,
                                             parent=parent)
            return CreateContentReply(success=True, reply=reply)
        except Exception as e:
            logger.info('create content reply error')
            logger.info('parent_id : '+str(parent_id))
            logger.info(e)
            return CreateContentReply(success=False)