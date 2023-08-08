from graphene_django import DjangoObjectType
from gym_student.models import AuditionDetail


class AuditionDetailType(DjangoObjectType):
    class Meta:
        model = AuditionDetail

