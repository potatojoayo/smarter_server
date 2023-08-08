import graphene

from authentication.models import User
from authentication.types import UserType
from authentication.types.user_input_type import UserInputType
from business.models import Gym, Agency
from business.types import GymType
from business.types.gym.gym_input_type import GymInputType
from django.contrib.auth.models import Group

from common.methods.send_notification import send_notification


class UpdateGym(graphene.Mutation):
    class Arguments:
        gym = GymInputType()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, gym):

        new_gym_user = User.objects.get(pk=gym.user.id)
        print(new_gym_user.is_active)
        print(gym.user.is_active)
        """if new_gym_user.is_active is False and gym.user.is_active is True:
            send_notification(user=new_gym_user, type='회원가입승인')
        """
        User.objects.filter(pk=gym.user.id).update(**gym.user)
        gym.pop('user', None)
        Gym.objects.filter(user=new_gym_user).update(**gym)

        return UpdateGym(success=True,)



