import graphene

from authentication.models import User


class CheckIsAdmin(graphene.Mutation):

    class Arguments:
        token = graphene.String()

    success = graphene.Boolean(default_value=False)

    @classmethod
    def mutate(cls, _, info, **kwargs):
        user: User = info.context.user
        print(user)
        return CheckIsAdmin(success=user.groups.filter(name='관리자').exists())


