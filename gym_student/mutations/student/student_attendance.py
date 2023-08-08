from datetime import datetime

import graphene

from gym_class.models import AttendanceDetail
from gym_student.methods.gym_send_notification import gym_send_notification


class StudentAttendance(graphene.Mutation):
    class Arguments:
        attendance_ids = graphene.List(graphene.Int)
        state = graphene.String()
        absent_reason = graphene.String()

    success = graphene.Boolean()

    @classmethod
    def mutate(cls, _, __, **kwargs):
        now = datetime.now()
        attendance_ids = kwargs.get('attendance_ids')
        state = kwargs.get('state')
        attendances = AttendanceDetail.objects.filter(pk__in=attendance_ids)
        attendances.update(type=state)
        if state == "결석":
            absent_reason = kwargs.get('absent_reason')
            attendances.update(absent_reason=absent_reason)
        elif state == "등원":
            attendances.update(date_attended=now)
            for attendance in attendances:
                gym_send_notification(user=attendance.student, type=state+"알림",
                                      attendance_hour=now.hour, attendance_min=now.minute)

        return StudentAttendance(success=True)
