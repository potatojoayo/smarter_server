import graphene

from authentication.models import User
from business.models import TaFirm


class CheckIsTa(graphene.Mutation):

    success = graphene.Boolean(default_value=False)

    @classmethod
    def mutate(cls, _, info):
        try:
            user: User = info.context.user
            return CheckIsTa(success=user.ta_firm is not None)
        except TaFirm.DoesNotExist:
            return CheckIsTa(success=False)


