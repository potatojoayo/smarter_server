from gym_class.types.attendance.attendance_type import AttendanceType
from graphene import relay


class AttendanceConnection(relay.Connection):
    class Meta:
        node = AttendanceType
