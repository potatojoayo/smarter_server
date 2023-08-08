import graphene
from django.contrib.auth.models import Group

from authentication.models import User
from authentication.types import UserType
from authentication.types.user_input_type import UserInputType


class CheckIsActive(graphene.Mutation):
    class Arguments:
        identification = graphene.String()

    is_active = graphene.Boolean()
    is_gym = graphene.Boolean(default_value=True)

    @classmethod
    def mutate(cls, _, info, identification=None):
        try:
            if identification:
                user = User.objects.get(identification=identification)
            else:
                user = info.context.user
            gym = Group.objects.get(name='체육관')
            if user in gym.user_set.all():
                return CheckIsActive(is_active=user.is_active)
            else:
                return CheckIsActive(is_gym=False, is_active=False)
        except:
            return CheckIsActive(is_active=False)
