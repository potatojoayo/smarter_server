import graphene
from django.utils import timezone

from cs.models import CsRequest


class UpdateCsRequestState(graphene.Mutation):
    class Arguments:
        cs_request_id = graphene.Int()
        state = graphene.String()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, cs_request_id, state):
        try:
            cs_request = CsRequest.objects.get(pk=cs_request_id)
            cs_request.cs_state = state
            if state == '처리완료':
                cs_request.date_completed = timezone.now()
            print(state)
            cs_request.save()

            return UpdateCsRequestState(success=True)
        except Exception as e:
            import logging
            logger = logging.getLogger('myLog')
            logger.info(e)
            return UpdateCsRequestState(success=False)