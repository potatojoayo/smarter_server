from graphene_django import DjangoObjectType

from gym_student.models import School


class SchoolType(DjangoObjectType):
    class Meta:
        model = School
