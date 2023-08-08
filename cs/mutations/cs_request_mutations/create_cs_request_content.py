import graphene

from cs.models import CsRequestContents, CsRequest
from cs.types.cs_request_content_type import CsRequestContentType


class CreateCsRequestContents(graphene.Mutation):
    class Arguments:
        cs_request_id = graphene.Int()
        contents = graphene.String()

    success = graphene.Boolean()
    cs_request_contents = graphene.List(CsRequestContentType)

    @classmethod
    def mutate(cls, _, __, cs_request_id, contents):
        try:
            cs_request = CsRequest.objects.get(pk=cs_request_id)
            CsRequestContents.objects.create(cs_request=cs_request,
                                             contents=contents)
            return CreateCsRequestContents(success=True,
                                           cs_request_contents=cs_request.
                                           request_contents.filter(is_deleted=False, parent__isnull=True).
                                           order_by('date_created'))
        except Exception as e:
            import logging
            logger = logging.getLogger('myLog')
            logger.info(e)
            return CreateCsRequestContents(success=False)
