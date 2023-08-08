import graphene
from django.db import transaction

from cs.models import CsRequestContents
from cs.types.cs_request_content_type import CsRequestContentType
from server.settings import logger


class UpdateCsRequestContents(graphene.Mutation):
    class Arguments:
        content_id = graphene.Int()
        contents = graphene.String()

    success = graphene.Boolean()
    cs_request_contents = graphene.Field(CsRequestContentType)

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, __, content_id, contents):
        try:
            cs_request_content = CsRequestContents.objects.get(pk=content_id)
            cs_request_content.contents = contents
            cs_request_content.save()
            return UpdateCsRequestContents(success=True, cs_request_contents=cs_request_content)
        except Exception as e:
            logger.info('update_cs_request_content')
            logger.info('content_id : '+str(content_id))
            logger.info(e)
            return UpdateCsRequestContents(success=False)
