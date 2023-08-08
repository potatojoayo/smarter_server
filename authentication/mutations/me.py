import graphene

from authentication.types import UserType


class Me(graphene.Mutation):

    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, _, info):
        return Me(user=info.context.user)
