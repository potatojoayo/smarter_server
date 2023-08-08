import graphene

from gym_class.models import Level
from gym_class.types import LevelType


class ChangeLevelOrder(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        increase = graphene.Boolean()

    success = graphene.Boolean()
    levels = graphene.List(LevelType)

    @classmethod
    def mutate(cls, _, info, id, increase):
        gym = info.context.user.gym
        level = Level.objects.get(pk=id)
        if increase:
            level_upper = Level.objects.get(gym=gym, order=level.order+1)
            level.order, level_upper.order = level_upper.order, level.order
            level_upper.save()
        else:
            level_below = Level.objects.get(gym=gym, order=level.order-1)
            level.order, level_below.order = level_below.order, level.order
            level_below.save()
        level.save()

        return ChangeLevelOrder(success=True, levels=Level.objects.filter(gym=gym).order_by('order'))
