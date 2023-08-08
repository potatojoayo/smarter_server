from graphene_django import DjangoObjectType
from graphene import relay
from gym_class.models import AttendanceDetail


class AttendanceType(DjangoObjectType):
    class Meta:
        model = AttendanceDetail
