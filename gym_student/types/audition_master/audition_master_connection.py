from graphene import relay

from gym_student.types.audition_master.audition_master_type import AuditionMasterType


class AuditionMasterConnection(relay.Connection):
    class Meta:
        node = AuditionMasterType
        