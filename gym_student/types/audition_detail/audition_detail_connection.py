from gym_student.types.audition_detail.audition_detail_type import AuditionDetailType
from graphene import relay


class AuditionDetailConnection(relay.Connection):
    class Meta:
        node = AuditionDetailType
