import graphene
from django.contrib.auth.models import Group

from authentication.models import User
from authentication.types import UserType
from authentication.types.user_input_type import UserInputType


class CheckIsParent(graphene.Mutation):
    class Arguments:
        identification = graphene.String()

    is_parent = graphene.Boolean()

    @classmethod
    def mutate(cls, _, info, identification=None):
        try:
            if identification:
                user = User.objects.get(identification=identification)
            else:
                user = info.context.user
            parent = Group.objects.get(name='학부모')
            if user in parent.user_set.all():
                return CheckIsParent(is_parent=True)
            else:
                return CheckIsParent(is_parent=False)
        except:
            return CheckIsParent(is_parent=False)
