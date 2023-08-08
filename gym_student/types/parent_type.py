from graphene_django import DjangoObjectType

from gym_student.models import Parent


class ParentType(DjangoObjectType):
    class Meta:
        model = Parent
