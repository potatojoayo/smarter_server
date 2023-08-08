import graphene

from authentication.models import User
from authentication.types import UserType
from authentication.types.user_input_type import UserInputType


class CreateOrUpdateUser(graphene.Mutation):
    class Arguments:
        user = UserInputType()


    user = graphene.Field(UserType)

    @classmethod
    def mutate(cls, _, __, user, password):
        if user.id:
            User.objects.filter(pk=user.id).update(**user,password=password)
        else:
            User.objects.create_user(**user, password=password)
