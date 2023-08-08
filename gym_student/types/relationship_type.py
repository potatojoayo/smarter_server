from graphene_django import DjangoObjectType

from gym_student.models import Relationship


class RelationshipType(DjangoObjectType):
    class Meta:
        model = Relationship
