import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from base_classes import CountableConnectionBase
from gym_class.models import AttendanceMaster
from gym_class.types.attendance.attendance_detail_type import AttendanceDetailType


class AttendanceMasterNode(DjangoObjectType):
    class Meta:
        model = AttendanceMaster
        interfaces = (relay.Node, )
        filter_fields = {'class_master__id': ['exact'],}
        connection_class = CountableConnectionBase

    attendance_master_id = graphene.Int()
    attendance_master_in = graphene.Int()
    attendance_master_absent = graphene.Int()
    attendance_master_late = graphene.Int()
    attendance_master_other_class = graphene.Int()
    attendance_master_all = graphene.Int()
    attendance_master_out = graphene.Int()
    details = graphene.List(AttendanceDetailType)
    my_children_details = graphene.List(AttendanceDetailType)

    @staticmethod
    def resolve_my_children_details(root, info):
        parent = info.context.user.parent
        return root.attendance_details.filter(student__parent=parent).order_by('id')

    @staticmethod
    def resolve_attendance_master_id(root, _):
        return root.id

    @staticmethod
    def resolve_attendance_master_in(root, _):
        return root.attendance_details.filter(type="등원").count()

    @staticmethod
    def resolve_attendance_master_absent(root, _):
        return root.attendance_details.filter(type="결석").count()

    @staticmethod
    def resolve_attendance_master_late(root, _):
        return root.attendance_details.filter(type="지각").count()

    @staticmethod
    def resolve_details(root, _):
        return root.attendance_details.all().order_by('id')

    @staticmethod
    def resolve_attendance_master_other_class(root, _):
        return root.attendance_details.filter(type="타수업등원").count()

    @staticmethod
    def resolve_attendance_master_all(root, _):
        return root.attendance_details.all().count()

    @staticmethod
    def resolve_attendance_master_out(root, _):
        return root.attendance_details.filter(type="하원").count()

