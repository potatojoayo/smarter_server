import graphene

from cs.models import CsRequestContents
from cs.types.cs_request_content_type import CsRequestContentType


class DeleteCsRequestContents(graphene.Mutation):
    class Arguments:
        cs_request_content_id = graphene.Int()

    success = graphene.Boolean()
    cs_request_contents = graphene.List(CsRequestContentType)

    @classmethod
    def mutate(cls, _, __, cs_request_content_id):
        try:
            contents = CsRequestContents.objects.get(pk=cs_request_content_id)
            cs_request = contents.cs_request
            contents.is_deleted = True
            contents.save()
            return DeleteCsRequestContents(success=True,
                                           cs_request_contents=cs_request.
                                           request_contents.filter(is_deleted=False).
                                           order_by('date_created'))
        except Exception as e:
            import logging
            logger = logging.getLogger('myLog')
            logger.info(e)
            return DeleteCsRequestContents(success=False)
