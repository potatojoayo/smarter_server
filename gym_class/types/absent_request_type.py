from graphene_django import DjangoObjectType

from gym_class.models import AbsentRequest


class AbsentRequestType(DjangoObjectType):

    class Meta:
        model = AbsentRequest



