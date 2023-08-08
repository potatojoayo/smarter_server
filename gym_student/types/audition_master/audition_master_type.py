from graphene_django import DjangoObjectType
from graphene import relay
from gym_student.models import AuditionMaster


class AuditionMasterType(DjangoObjectType):
    class Meta:
        model = AuditionMaster
        interface = (relay.Node,)

