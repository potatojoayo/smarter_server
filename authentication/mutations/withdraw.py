import graphene
from django.db import transaction


class Withdraw(graphene.Mutation):

    success = graphene.Boolean()

    @classmethod
    @transaction.atomic()
    def mutate(cls, _, info):
        user = info.context.user
        user.is_active = False
        user.save()
        return Withdraw(success=True)



