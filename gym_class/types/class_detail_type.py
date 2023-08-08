from graphene_django import DjangoObjectType

from gym_class.models import ClassDetail


class ClassDetailType(DjangoObjectType):

    class Meta:
        model = ClassDetail


