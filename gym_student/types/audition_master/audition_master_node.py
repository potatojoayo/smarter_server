import graphene
from graphene_django import DjangoObjectType
from graphene import relay

from base_classes import CountableConnectionBase
from gym_student.models import AuditionMaster
from gym_student.types.audition_detail.audition_detail_type import AuditionDetailType


class AuditionMasterNode(DjangoObjectType):
    class Meta:
        model = AuditionMaster
        interfaces = (relay.Node,)
        filter_fields = {
        }
        connection_class = CountableConnectionBase

    audition_master_id = graphene.Int()
    details = graphene.List(AuditionDetailType)
    my_children_details = graphene.List(AuditionDetailType)

    @staticmethod
    def resolve_my_children_details(root, info):
        parent = info.context.user.parent
        return root.audition_details.filter(student__parent=parent).order_by('id')

    @staticmethod
    def resolve_details(root, _):
        return root.audition_details.all().order_by('id')

    @staticmethod
    def resolve_audition_master_id(root, __):
        return root.id

