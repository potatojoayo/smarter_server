from graphene_django import DjangoObjectType

from gym_class.models import Level


class LevelType(DjangoObjectType):

    class Meta:
        model = Level
